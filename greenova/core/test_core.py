import logging

from core.constants import AUTH_NAVIGATION, USER_NAVIGATION
from core.mixins import BreadcrumbMixin, PageTitleMixin
from core.signals import handle_user_update, log_user_login, log_user_logout
from core.templatetags.core_tags import auth_menu
from core.utils.roles import (ProjectRole, get_role_choices, get_role_color,
                              get_role_display)
from django.contrib.auth import get_user_model
from django.template import Context
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)
User = get_user_model()

class CoreBaseTestCase(TestCase):
    """Base test case for core app tests."""

    @classmethod
    def setUpClass(cls):
        """Set up test data for all tests."""
        super().setUpClass()
        cls.factory = RequestFactory()
        cls.users = {
            'superuser': User.objects.create_superuser(
                'admin', 'admin@example.com', 'adminpassword'
            ),
            'regular_user': User.objects.create_user(
                'regular', 'regular@example.com', 'userpassword', is_active=True
            )
        }

    def setUp(self):
        """Set up test data for each test."""
        super().setUp()
        self.request = self.factory.get('/')
        self.request.user = self.users['regular_user']

# ----- VIEW TESTS -----

class TestCoreViews(CoreBaseTestCase):
    """Test core views functionality."""

    def test_home_view(self):
        """Test the home view."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing/index.html')

    def test_health_check_view(self):
        """Test health check view."""
        url = reverse('core:health_check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'ok')

# ----- MIXIN TESTS -----

class TestCoreMixins(CoreBaseTestCase):
    """Test core mixins functionality."""

    def test_breadcrumb_mixin(self):
        """Test BreadcrumbMixin adds breadcrumbs to context."""
        class TestView(BreadcrumbMixin, TemplateView):
            template_name = 'test.html'
            breadcrumbs = [('Home', 'home'), ('Test', None)]

        view = TestView()
        view.setup(self.request)  # Initialize view with request
        context = view.get_context_data()
        self.assertIn('breadcrumbs', context)
        self.assertEqual(context['breadcrumbs'], [('Home', 'home'), ('Test', None)])

    def test_page_title_mixin(self):
        """Test PageTitleMixin adds page title to context."""
        class TestView(PageTitleMixin, TemplateView):
            template_name = 'test.html'
            page_title = 'Test Page'

        view = TestView()
        view.setup(self.request)  # Initialize view with request
        context = view.get_context_data()
        self.assertIn('page_title', context)
        self.assertEqual(context['page_title'], 'Test Page')

# ----- TEMPLATETAG TESTS -----

class TestCoreTemplateTags(CoreBaseTestCase):
    """Test core template tags functionality."""

    def test_auth_menu_authenticated(self):
        """Test auth_menu template tag with authenticated user."""
        context = Context({'request': self.request})
        result = auth_menu(context)
        self.assertTrue(result['is_authenticated'])
        self.assertEqual(result['user_display_name'], 'regular')
        self.assertEqual(result['user_navigation'], USER_NAVIGATION)

    def test_auth_menu_anonymous(self):
        """Test auth_menu template tag with anonymous user."""
        request = self.factory.get('/')
        request.user = None
        context = Context({'request': request})
        result = auth_menu(context)
        self.assertFalse(result['is_authenticated'])
        self.assertEqual(result['auth_navigation'], AUTH_NAVIGATION)

# ----- UTILITY TESTS -----

class TestCoreUtils(CoreBaseTestCase):
    """Test core utility functions."""

    def test_role_utility_functions(self):
        """Test role utility functions."""
        self.assertEqual(get_role_display(ProjectRole.OWNER.value), 'Owner')
        self.assertEqual(get_role_color(ProjectRole.OWNER.value), 'success')
        role_choices = get_role_choices()
        self.assertIsInstance(role_choices, list)
        self.assertTrue(role_choices)
        self.assertTrue(all(isinstance(choice, tuple) and len(choice) == 2
                            for choice in role_choices))

# ----- SIGNAL TESTS -----

class TestCoreSignals(CoreBaseTestCase):
    """Test core signal handlers."""

    def test_user_signals(self):
        """Test user-related signal handlers."""
        user = self.users['regular_user']
        # Test login signal
        log_user_login(None, self.request, user)
        # Test logout signal
        log_user_logout(None, self.request, user)
        # Test update signal
        handle_user_update(User, user, False)
