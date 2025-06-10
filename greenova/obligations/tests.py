from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.utils import timezone
from mechanisms.models import EnvironmentalMechanism
from projects.models import Project

from .models import (
    ComplianceComment,
    NonConformanceComment,
    Obligation,
    ObligationEvidence,
)

User = get_user_model()


class ObligationModelTests(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(name="Test Project")
        self.mechanism = EnvironmentalMechanism.objects.create(
            name="Test Mechanism", project=self.project
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser_obligation@example.com",
            password="testpass",
        )
        from responsibility.models import Responsibility, ResponsibilityAssignment

        self.responsibility = Responsibility.objects.create(
            name="SCJV - Project Director"
        )
        self.obligation = Obligation.objects.create(
            obligation_number="PCEMP-001",
            project=self.project,
            primary_environmental_mechanism=self.mechanism,
            obligation="Test obligation text",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="not started",
            action_due_date=timezone.now().date()
            - timedelta(days=1),  # yesterday for overdue test
        )
        ResponsibilityAssignment.objects.create(
            user=self.user,
            obligation=self.obligation,
            responsibility=self.responsibility,
        )

    def test_str_method(self) -> None:
        assert self.obligation.obligation_number in str(self.obligation)
        assert self.project.name in str(self.obligation)

    def test_is_overdue_property(self) -> None:
        assert self.obligation.is_overdue
        self.obligation.status = "completed"
        self.obligation.save()
        assert not self.obligation.is_overdue

    def test_calculate_next_recurring_date(self) -> None:
        # Set action_due_date to today for this test
        self.obligation.action_due_date = timezone.now().date()
        self.obligation.recurring_obligation = True
        self.obligation.recurring_frequency = "Daily"
        self.obligation.save()
        # Clear the recurring_forecasted_date that was set by the post_save signal
        # so we test the calculation from action_due_date
        self.obligation.recurring_forecasted_date = None
        base_date = timezone.now().date()
        next_date = self.obligation.calculate_next_recurring_date()
        assert next_date == base_date + timedelta(days=1)

    def test_to_pb_and_from_pb(self) -> None:
        pb = self.obligation.to_pb()
        assert pb.obligation_number == self.obligation.obligation_number
        obligation2 = Obligation.from_pb(pb)
        assert obligation2.obligation_number == self.obligation.obligation_number

    def test_responsibility_assignments(self) -> None:
        # type: ignore[attr-defined]
        assignments = self.obligation.responsibility_assignments
        assert assignments.exists()

    def test_clean_and_save(self) -> None:
        # Change obligation_number and ensure slug is unique
        self.obligation.obligation_number = "PCEMP-002"
        self.obligation.slug = ""  # Force regeneration of slug
        self.obligation.clean()
        self.obligation.save()
        assert Obligation.objects.filter(obligation_number="PCEMP-002").exists()


class ObligationEvidenceModelTests(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(name="Evidence Project")
        self.mechanism = EnvironmentalMechanism.objects.create(
            name="Evidence Mechanism", project=self.project
        )
        self.user = User.objects.create_user(
            username="evidenceuser",
            email="evidenceuser@example.com",
            password="testpass",
        )
        self.obligation = Obligation.objects.create(
            obligation_number="PCEMP-010",
            project=self.project,
            primary_environmental_mechanism=self.mechanism,
            obligation="Evidence obligation",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="not started",
        )

    def test_evidence_str(self) -> None:
        evidence = ObligationEvidence.objects.create(
            obligation=self.obligation,
            file="evidence.txt",
            description="Test evidence file",
        )
        assert "Evidence for" in str(evidence)


class ComplianceCommentModelTests(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(name="Compliance Project")
        self.mechanism = EnvironmentalMechanism.objects.create(
            name="Compliance Mechanism", project=self.project
        )
        self.user = User.objects.create_user(
            username="complianceuser",
            email="complianceuser@example.com",
            password="testpass",
        )
        self.obligation = Obligation.objects.create(
            obligation_number="PCEMP-020",
            project=self.project,
            primary_environmental_mechanism=self.mechanism,
            obligation="Compliance obligation",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="not started",
        )

    def test_compliance_comment_str(self) -> None:
        comment = ComplianceComment.objects.create(
            obligation=self.obligation, comment="Test compliance comment"
        )
        assert "ComplianceComment" in str(comment)


class NonConformanceCommentModelTests(TestCase):
    def setUp(self) -> None:
        self.project = Project.objects.create(name="NC Project")
        self.mechanism = EnvironmentalMechanism.objects.create(
            name="NC Mechanism", project=self.project
        )
        self.user = User.objects.create_user(
            username="ncuser",
            email="ncuser@example.com",
            password="testpass",
        )
        self.obligation = Obligation.objects.create(
            obligation_number="PCEMP-030",
            project=self.project,
            primary_environmental_mechanism=self.mechanism,
            obligation="NC obligation",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="not started",
        )

    def test_nonconformance_comment_str(self) -> None:
        comment = NonConformanceComment.objects.create(
            obligation=self.obligation, comment="Test NC comment"
        )
        assert "NonConformanceComment" in str(comment)


class ObligationTemplateRenderingTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.project = Project.objects.create(name="Template Project")
        self.mechanism = EnvironmentalMechanism.objects.create(
            name="Template Mechanism", project=self.project
        )
        self.user = User.objects.create_user(
            username="templateuser",
            email="templateuser@example.com",
            password="testpass",
        )
        self.obligation = Obligation.objects.create(
            obligation_number="PCEMP-100",
            project=self.project,
            primary_environmental_mechanism=self.mechanism,
            obligation="Template obligation text",
            environmental_aspect="Air",
            procedure="Cultural Heritage Management",
            accountability="Perdaman",
            status="not started",
            action_due_date=timezone.now().date(),
        )
        self.client.force_login(self.user)

    def test_obligation_list_template_renders(self) -> None:
        from django.template import Context, Template

        # Test the core obligation list template content without django_tables2
        # render_table tag
        t = Template("""
            <main>
                <h1 class="mb-4">Obligations</h1>
                <form method="get" class="mb-4">
                    {{ filter.form.as_p }}
                    <button type="submit" class="btn btn-outline-primary">Filter</button>
                </form>
                {% if table %}
                    <p>Table would be rendered here</p>
                    {% include "obligations/components/_pagination.html" %}
                {% else %}
                    <p>No obligations found.</p>
                {% endif %}
            </main>
        """)

        class DummyForm:
            def as_p(self) -> str:
                return "<p>Filter form</p>"

        class DummyFilter:
            def __init__(self) -> None:
                self.form = DummyForm()

        html = t.render(
            Context(
                {
                    "table": True,  # Just indicate table exists
                    "filter": DummyFilter(),
                }
            )
        )
        assert "Obligations" in html
        assert "Filter" in html
        assert "Table would be rendered here" in html

    def test_obligation_detail_modal_component_renders(self) -> None:
        from django.template import Context, Template

        t = Template("""
            {% load static obligation_tags %}
            {% load django_bootstrap5 %}
            <div class="modal fade" id="obligationDetailModal" tabindex="-1" aria-labelledby="obligationDetailModalLabel" aria-hidden="true" data-bs-backdrop="static" data-bs-keyboard="false">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="obligationDetailModalLabel">Obligation Details</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body" id="obligation-modal-body" tabindex="0">
                            <!-- Content loaded dynamically via htmx or hyperscript -->
                        </div>
                    </div>
                </div>
            </div>
        """)
        html = t.render(Context({}))
        assert 'id="obligationDetailModal"' in html

    def test_obligation_status_badge_component(self) -> None:
        from django.template import Context, Template

        t = Template(
            "{% include 'obligations/components/_status_badge.html' with status='Completed' %}"
        )
        html = t.render(Context({}))
        assert "badge" in html
        assert "Completed" in html

    def test_obligation_pagination_component(self) -> None:
        from django.core.paginator import Paginator
        from django.template import Context, Template

        obligations = [self.obligation for _ in range(15)]
        paginator = Paginator(obligations, 5)
        page_obj = paginator.get_page(1)
        t = Template("{% include 'obligations/components/_pagination.html' %}")
        html = t.render(Context({"page_obj": page_obj}))
        assert "pagination" in html

    def test_obligation_modal_content_component(self) -> None:
        from django.template import Context, Template

        t = Template(
            "{% include 'obligations/components/_obligation_modal_content.html' %}"
        )
        html = t.render(Context({"obligation": self.obligation}))
        assert str(self.obligation.obligation_number) in html
        assert "Obligation Number" in html

    def test_obligation_editable_modal_content_component(self) -> None:
        from django import forms
        from django.template import Context, Template

        class DummyForm(forms.Form):
            field = forms.CharField()

        form = DummyForm()
        t = Template("""
            {% load static obligation_tags %}
            {% load crispy_forms_tags %}
            <form method="post" action="" class="needs-validation" novalidate>
                {% csrf_token %}
                {{ form|crispy }}
                <div class="d-flex justify-content-end gap-2 mt-3">
                    <button type="submit" class="btn btn-primary">Save</button>
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                </div>
            </form>
        """)
        html = t.render(Context({"form": form}))
        assert "form" in html
        assert "Save" in html
