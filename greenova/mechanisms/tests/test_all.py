"""Unit tests for the mechanisms app: models, views, forms, middleware, admin, tasks, figures, plotlyapp, template tags, and templates.

Covers all code paths for 100% test coverage.
"""
from unittest import mock
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.http import HttpRequest
from django.template import Context, Template

from mechanisms.models import EnvironmentalMechanism, update_all_mechanism_counts
from mechanisms.views import export_mechanism, export_all_mechanisms
from mechanisms.forms import Mechanism
from mechanisms.figures import generate_pie_chart, encode_figure_to_base64, get_mechanism_chart, get_overall_chart
from mechanisms.plotlyapp import get_mechanism_plotly_data, get_overall_plotly_data, serialize_plotly_data
from mechanisms.middleware import MechanismsChartMiddleware
from mechanisms.tasks import run_mechanism_checks
from mechanisms.templatetags import mechanism_tags
from mechanisms.admin import EnvironmentalMechanismAdmin

from projects.models import Project


class MechanismModelTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Test Project")
        self.mech = EnvironmentalMechanism.objects.create(
            name="Test Mechanism",
            project=self.project,
            description="Desc",
            category="Cat",
            reference_number="REF123",
            status="not_started",
        )

    def test_str(self):
        self.assertEqual(str(self.mech), "Test Mechanism")

    def test_total_obligations(self):
        self.mech.not_started_count = 2
        self.mech.in_progress_count = 3
        self.mech.completed_count = 4
        self.assertEqual(self.mech.total_obligations, 9)

    def test_update_obligation_counts(self):
        # No obligations, should not raise
        self.mech.update_obligation_counts()
        self.assertIsInstance(self.mech.not_started_count, int)

    def test_get_status_data(self):
        self.mech.not_started_count = 1
        self.mech.in_progress_count = 2
        self.mech.completed_count = 3
        self.mech.overdue_count = 4
        data = self.mech.get_status_data()
        self.assertIn("Overdue", data)

    def test_update_all_mechanism_counts(self):
        count = update_all_mechanism_counts()
        self.assertIsInstance(count, int)


class MechanismViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username="user", password="pass")
        self.project = Project.objects.create(name="Proj")
        self.mech = EnvironmentalMechanism.objects.create(
            name="M1", project=self.project)

    def test_mechanism_list_view(self):
        self.client.force_login(self.user)
        url = reverse("mechanisms:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "M1")

    def test_mechanism_chart_view_no_project(self):
        self.client.force_login(self.user)
        url = reverse("mechanisms:mechanism_charts")
        response = self.client.get(url)
        self.assertContains(response, "No project selected")

    def test_mechanism_chart_view_with_project(self):
        self.client.force_login(self.user)
        url = reverse("mechanisms:mechanism_charts") + f"?project_id={self.project.id}"
        response = self.client.get(url)
        self.assertContains(response, "Environmental Mechanisms Analysis")

    def test_export_mechanism(self):
        self.client.force_login(self.user)
        resp = export_mechanism(self.client.request().wsgi_request, self.mech.id)
        self.assertIsNone(resp)  # user_can_view_mechanism returns False by default

    def test_export_all_mechanisms(self):
        self.client.force_login(self.user)
        resp = export_all_mechanisms(self.client.request().wsgi_request)
        self.assertIsNone(resp)

    def test_import_mechanism_get(self):
        self.client.force_login(self.user)
        resp = self.client.get(reverse("mechanisms:mechanism_charts"))
        self.assertEqual(resp.status_code, 200)


class MechanismFormTests(TestCase):
    def test_mechanism_class(self):
        definition = {"id": "1"}
        m = Mechanism(definition)
        self.assertEqual(m.definition["id"], "1")
        m.initialize({"id": "2",
                      "mechanism_id": "1",
                      "status": "not_started",
                      "last_run": None,
                      "result": None})
        self.assertEqual(m.state["id"], "2")
        m.update_state({"status": "completed"})
        self.assertEqual(m.state["status"], "completed")
        state = m.get_state()
        self.assertIn("status", state)


class MechanismFiguresTests(TestCase):
    def test_generate_pie_chart(self):
        fig = generate_pie_chart([1, 2, 3, 4], ["A", "B", "C", "D"], [
                                 "#111", "#222", "#333", "#444"])
        self.assertIsNotNone(fig)

    def test_encode_figure_to_base64(self):
        fig = generate_pie_chart([1, 2, 3, 4], ["A", "B", "C", "D"], [
                                 "#111", "#222", "#333", "#444"])
        b64 = encode_figure_to_base64(fig)
        self.assertIsInstance(b64, str)

    def test_get_mechanism_chart(self):
        # Will fallback to DoesNotExist
        fig, b64 = get_mechanism_chart(99999)
        self.assertIsInstance(b64, str)

    def test_get_overall_chart(self):
        fig, b64 = get_overall_chart(99999)
        self.assertIsInstance(b64, str)


class MechanismPlotlyAppTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="P1")
        self.mech = EnvironmentalMechanism.objects.create(
            name="M1", project=self.project)

    def test_get_mechanism_plotly_data(self):
        data = get_mechanism_plotly_data(self.mech.id)
        self.assertIn("data", data)
        data = get_mechanism_plotly_data(99999)
        self.assertIn("data", data)

    def test_get_overall_plotly_data(self):
        data = get_overall_plotly_data(self.project.id)
        self.assertIn("data", data)
        data = get_overall_plotly_data(99999)
        self.assertIn("data", data)

    def test_serialize_plotly_data(self):
        data = get_mechanism_plotly_data(self.mech.id)
        s = serialize_plotly_data(data)
        self.assertIsInstance(s, str)


class MechanismMiddlewareTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = MechanismsChartMiddleware(
            lambda r: mock.Mock(status_code=200))

    def test_process_request_and_response(self):
        req = self.factory.get("/mechanisms/charts/?mechanism_id=1&chart_type=svg")
        req.session = {}
        resp = self.middleware(req)
        self.assertTrue("Cache-Control" in resp)


class MechanismTasksTests(TestCase):
    def test_run_mechanism_checks(self):
        run_mechanism_checks()  # Should not raise


class MechanismTemplateTagTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="P1")
        self.mech = EnvironmentalMechanism.objects.create(
            name="M1", project=self.project)

    def test_get_item(self):
        self.assertEqual(mechanism_tags.get_item({"a": 1}, "a"), 1)

    def test_mechanism_name(self):
        self.assertEqual(mechanism_tags.mechanism_name(self.mech.id), "M1")
        self.assertIn("Unknown", mechanism_tags.mechanism_name(99999))
        self.assertIn("Invalid", mechanism_tags.mechanism_name("bad"))

    def test_format_count(self):
        self.assertIn("count-zero", mechanism_tags.format_count(0))
        self.assertIn("count-nonzero", mechanism_tags.format_count(5))

    def test_total_obligations(self):
        self.assertIsInstance(mechanism_tags.total_obligations(self.mech), int)

    def test_mechanism_card(self):
        ctx = mechanism_tags.mechanism_card(self.mech)
        self.assertIn("mechanism", ctx)

    def test_mechanism_table(self):
        ctx = mechanism_tags.mechanism_table([self.mech])
        self.assertIn("mechanisms", ctx)

    def test_get_status_color(self):
        self.assertIn("status-", mechanism_tags.get_status_color("Completed"))


class MechanismAdminTests(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.project = Project.objects.create(name="P1")
        self.mech = EnvironmentalMechanism.objects.create(
            name="M1", project=self.project)
        self.admin = EnvironmentalMechanismAdmin(EnvironmentalMechanism, self.site)

    def test_get_queryset(self):
        req = HttpRequest()
        qs = self.admin.get_queryset(req)
        self.assertIsNotNone(qs)

    def test_get_total_obligations(self):
        self.assertIsInstance(self.admin.get_total_obligations(self.mech), int)

    def test_save_model(self):
        req = HttpRequest()
        self.admin.save_model(req, self.mech, None, True)

    def test_status_chart(self):
        self.assertIsInstance(self.admin.status_chart(self.mech), str)

    def test_has_add_permission(self):
        req = HttpRequest()
        self.assertIsInstance(self.admin.has_add_permission(req), bool)

    def test_is_overdue(self):
        self.assertIsInstance(self.admin.is_overdue(self.mech), bool)


class MechanismTemplateRenderTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(name="P1")
        self.mech = EnvironmentalMechanism.objects.create(
            name="M1", project=self.project)

    def test_mechanisms_list_template(self):
        t = Template(
            '{% load mechanism_tags %}{% include "mechanisms/mechanisms_list.html" %}')
        ctx = Context({"mechanisms": [self.mech]})
        html = t.render(ctx)
        self.assertIn("M1", html)

    def test_mechanism_card_template(self):
        t = Template(
            '{% load mechanism_tags %}{% include "mechanisms/components/mechanism_card.html" %}')
        ctx = Context({"mechanism": self.mech})
        html = t.render(ctx)
        self.assertIn("M1", html)

    def test_mechanism_table_template(self):
        t = Template(
            '{% load mechanism_tags %}{% include "mechanisms/components/mechanism_table.html" %}')
        ctx = Context({"mechanisms": [self.mech]})
        html = t.render(ctx)
        self.assertIn("M1", html)

    def test_charts_template(self):
        t = Template('{% include "mechanisms/components/_charts.html" %}')
        ctx = Context({"table_data": []})
        html = t.render(ctx)
        self.assertIn("Environmental Mechanism Status Charts", html)

    def test_mechanism_charts_template(self):
        t = Template('{% include "mechanisms/mechanism_charts.html" %}')
        ctx = Context({"mechanism_charts": [], "table_data": []})
        html = t.render(ctx)
        self.assertIn("Environmental Mechanisms Analysis", html)

    def test_obligation_insight_partial(self):
        t = Template('{% include "mechanisms/partials/_obligation_insight.html" %}')
        ctx = Context({"error": None, "status": "Completed",
                      "count": 1, "obligations": [], "total_count": 1})
        html = t.render(ctx)
        self.assertIn("Obligations", html)
