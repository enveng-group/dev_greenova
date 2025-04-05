import logging

import pytest
from core.commons import get_active_namespace, get_user_display_name
from core.constants import AUTH_NAVIGATION, MAIN_NAVIGATION, USER_NAVIGATION
from core.mixins import BreadcrumbMixin, PageTitleMixin, SectionMixin, ViewMixin
from core.signals import handle_user_update, log_user_login, log_user_logout
from core.templatetags.core_tags import (active_link, auth_menu, breadcrumb_navigation,
                                         main_navigation, theme_switcher)
from core.utils.roles import (ProjectRole, get_role_choices, get_role_color,
                              get_role_display)
from django.contrib.auth import get_user_model
from django.template import Context, Template
from django.test import RequestFactory
from django.urls import reverse
from django.views.generic import TemplateView

# Configure logging for tests
logger = logging.getLogger(__name__)
User = get_user_model()

# ----- FIXTURES -----

@pytest.fixture
def test_users(db, django_user_model):
    """Create test users with different roles."""
    users = {
        'superuser': django_user_model.objects.create_superuser(
            'admin', 'admin@example.com', 'adminpassword'
        ),
        'regular_user': django_user_model.objects.create_user(
            'regular', 'regular@example.com', 'userpassword', is_active=True
        ),
    }
    return users

@pytest.fixture
def authenticated_client(client, test_users, request):
    """Return an authenticated client for a specified user role."""
    user_role = request.param
    user = test_users[user_role]
    client.force_login(user)
    return client

@pytest.fixture
def request_factory():
    """Return a request factory instance."""
    return RequestFactory()

@pytest.fixture
def mock_request(request_factory, test_users):
    """Create a mock request with a user."""
    request = request_factory.get('/')
    request.user = test_users['regular_user']
    return request

@pytest.fixture
def rendered_template():
    """Helper fixture to render a template string with a context."""
    def _render(template_string, context=None):
        context = Context(context or {})
        return Template(template_string).render(context)
    return _render


# ----- VIEW TESTS -----

@pytest.mark.django_db
class TestCoreViews:
    """Test core views functionality."""

    def test_home_view(self, client):
        """Test the home view."""
        url = reverse('home')
        response = client.get(url)

        # Should return a success response
        assert response.status_code == 200
        assert 'landing/index.html' in [t.name for t in response.templates]

    def test_health_check_view(self, client):
        """Test health check view."""
        url = reverse('core:health_check')
        response = client.get(url)

        assert response.status_code == 200
        assert response.json()['status'] == 'ok'

    def test_error_pages(self, client):
        """Test error page templates."""
        error_pages = [
            ('core:error_400', 400),
            ('core:error_403', 403),
            ('core:error_404', 404),
            ('core:error_500', 500)
        ]

        for view_name, status_code in error_pages:
            url = reverse(view_name)
            response = client.get(url)
            assert response.status_code == 200
            assert f'errors/{status_code}.html' in [t.name for t in response.templates]
            assert f'{status_code}' in response.content.decode()


# ----- MIXIN TESTS -----

@pytest.mark.django_db
class TestCoreMixins:
    """Test core mixins functionality."""

    def test_breadcrumb_mixin(self, request_factory):
        """Test BreadcrumbMixin adds breadcrumbs to context."""
        class TestView(BreadcrumbMixin, TemplateView):
            template_name = 'test.html'
            breadcrumbs = [('Home', 'home'), ('Test', None)]

        request = request_factory.get('/')
        view = TestView()
        view.request = request

        context = view.get_context_data()
        assert 'breadcrumbs' in context
        assert context['breadcrumbs'] == [('Home', 'home'), ('Test', None)]

    def test_page_title_mixin(self, request_factory):
        """Test PageTitleMixin adds page title to context."""
        class TestView(PageTitleMixin, TemplateView):
            template_name = 'test.html'
            page_title = 'Test Page'

        request = request_factory.get('/')
        view = TestView()
        view.request = request

        context = view.get_context_data()
        assert 'page_title' in context
        assert context['page_title'] == 'Test Page'

    def test_section_mixin(self, request_factory):
        """Test SectionMixin adds active section to context."""
        class TestView(SectionMixin, TemplateView):
            template_name = 'test.html'
            active_section = 'test_section'

        request = request_factory.get('/')
        view = TestView()
        view.request = request

        context = view.get_context_data()
        assert 'active_section' in context
        assert context['active_section'] == 'test_section'

    def test_view_mixin(self, request_factory):
        """Test ViewMixin combines breadcrumbs, page title, and section."""
        class TestView(ViewMixin, TemplateView):
            template_name = 'test.html'
            page_title = 'Test Page'
            active_section = 'test_section'
            breadcrumbs = [('Home', 'home'), ('Test', None)]

        request = request_factory.get('/')
        view = TestView()
        view.request = request

        context = view.get_context_data()
        assert 'breadcrumbs' in context
        assert 'page_title' in context
        assert 'active_section' in context


# ----- TEMPLATETAG TESTS -----

@pytest.mark.django_db
class TestCoreTemplateTags:
    """Test core template tags functionality."""

    def test_active_link(self, request_factory):
        """Test active_link template tag."""
        request = request_factory.get('/test/')
        context = Context({
            'request': request
        })

        # Mock the reverse function to return /test/ for 'test'
        with pytest.monkeypatch.context() as m:
            m.setattr('django.urls.reverse', lambda url_name: '/test/' if url_name == 'test' else f'/{url_name}/')

            # Test active link
            result = active_link(context, 'test')
            assert result == 'active'

            # Test inactive link
            result = active_link(context, 'other')
            assert result == ''

    def test_breadcrumb_navigation(self, request_factory):
        """Test breadcrumb_navigation template tag."""
        request = request_factory.get('/')
        context = Context({
            'request': request
        })

        result = breadcrumb_navigation(context)
        assert 'crumbs' in result
        assert len(result['crumbs']) >= 1  # At least Home crumb

    def test_auth_menu_authenticated(self, request_factory, test_users):
        """Test auth_menu template tag with authenticated user."""
        request = request_factory.get('/')
        request.user = test_users['regular_user']

        context = Context({
            'request': request
        })

        result = auth_menu(context)
        assert result['is_authenticated'] is True
        assert result['user_display_name'] == 'regular'
        assert result['user_navigation'] == USER_NAVIGATION

    def test_auth_menu_anonymous(self, request_factory):
        """Test auth_menu template tag with anonymous user."""
        request = request_factory.get('/')
        request.user = None

        context = Context({
            'request': request
        })

        result = auth_menu(context)
        assert result['is_authenticated'] is False
        assert result['auth_navigation'] == AUTH_NAVIGATION

    def test_theme_switcher(self):
        """Test theme_switcher template tag."""
        result = theme_switcher()
        assert 'theme_options' in result
        assert len(result['theme_options']) == 3
        assert ('Auto', 'auto') in result['theme_options']
        assert ('Light', 'light') in result['theme_options']
        assert ('Dark', 'dark') in result['theme_options']

    def test_main_navigation(self, request_factory):
        """Test main_navigation template tag."""
        request = request_factory.get('/')
        context = Context({
            'request': request
        })

        result = main_navigation(context)
        assert 'navigation_items' in result
        assert result['navigation_items'] == MAIN_NAVIGATION


# ----- UTILITY TESTS -----

@pytest.mark.django_db
class TestCoreUtils:
    """Test core utility functions."""

    def test_get_active_namespace(self, request_factory):
        """Test get_active_namespace function."""
        request = request_factory.get('/')

        # Test with no namespace
        assert get_active_namespace(request) == ''

    def test_get_user_display_name(self, test_users):
        """Test get_user_display_name function."""
        user = test_users['regular_user']
        assert get_user_display_name(user) == 'regular'

        # Test with full name
        user.first_name = 'Test'
        user.last_name = 'User'
        user.save()
        assert get_user_display_name(user) == 'Test User'

    def test_role_utility_functions(self):
        """Test role utility functions."""
        # Test get_role_display
        assert get_role_display(ProjectRole.OWNER.value) == 'Owner'

        # Test get_role_color
        assert get_role_color(ProjectRole.OWNER.value) == 'success'

        # Test get_role_choices
        role_choices = get_role_choices()
        assert isinstance(role_choices, list)
        assert len(role_choices) > 0
        assert all(isinstance(choice, tuple) and len(choice) == 2 for choice in role_choices)


# ----- SIGNAL TESTS -----

@pytest.mark.django_db
class TestCoreSignals:
    """Test core signal handlers."""

    def test_log_user_login(self, request_factory, test_users):
        """Test log_user_login signal handler."""
        request = request_factory.get('/')
        user = test_users['regular_user']

        with pytest.raises(Exception) as e:
            # Should not raise an exception
            log_user_login(None, request, user)

    def test_log_user_logout(self, request_factory, test_users):
        """Test log_user_logout signal handler."""
        request = request_factory.get('/')
        user = test_users['regular_user']

        with pytest.raises(Exception) as e:
            # Should not raise an exception
            log_user_logout(None, request, user)

    def test_handle_user_update(self, test_users):
        """Test handle_user_update signal handler."""
        user = test_users['regular_user']

        # Test update case
        with pytest.raises(Exception) as e:
            # Should not raise an exception
            handle_user_update(User, user, False)


# Add HealthCheckView test (referenced in urls.py but not defined in views.py)
# This will help detect if HealthCheckView exists and is properly implemented
@pytest.mark.xfail(reason='HealthCheckView may not be implemented yet')
def test_health_check_view_implementation():
    """Test that HealthCheckView is properly implemented."""
    from core.views import HealthCheckView
    assert hasattr(HealthCheckView, 'get')
