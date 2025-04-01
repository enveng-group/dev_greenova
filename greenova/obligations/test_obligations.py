import json
from datetime import date, timedelta

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from mechanisms.models import EnvironmentalMechanism
from obligations.forms import EvidenceUploadForm, ObligationForm
from obligations.models import Obligation, ObligationEvidence
from obligations.utils import (get_obligation_status, is_obligation_overdue,
                               normalize_frequency)
from projects.models import Project
from responsibility.models import Responsibility
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

# FIXTURES
@pytest.fixture
def test_user(db):
    """Create and return a test user."""
    user = User.objects.create_user(
        username='test',
        email='test@example.com',
        password='password'
    )
    return user

@pytest.fixture
def test_admin(db):
    """Create and return an admin user with all permissions."""
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass'
    )
    return admin

@pytest.fixture
def test_project(db):
    """Create and return a test project."""
    project = Project.objects.create(
        name='Test Project',
        description='A test project for unit testing'
    )
    return project

@pytest.fixture
def test_mechanism(db, test_project):
    """Create and return a test environmental mechanism."""
    mechanism = EnvironmentalMechanism.objects.create(
        name='Test Mechanism',
        project=test_project,
        reference_number='TEST-MECH-001'
    )
    return mechanism

@pytest.fixture
def test_responsibility(db):
    """Create and return a test responsibility."""
    responsibility = Responsibility.objects.create(
        name='Test Responsibility',
        description='A test responsibility'
    )
    return responsibility

@pytest.fixture
def test_obligation(db, test_project, test_mechanism, test_responsibility):
    """Create and return a test obligation."""
    obligation = Obligation.objects.create(
        obligation_number='PCEMP-001',
        project=test_project,
        primary_environmental_mechanism=test_mechanism,
        environmental_aspect='Air',
        obligation='Test obligation requirement',
        accountability='Perdaman',
        responsibility='SCJV - Environmental Lead',
        project_phase='Construction',
        action_due_date=timezone.now().date() + timedelta(days=30),
        status='not started'
    )
    # Add the responsibility relationship
    obligation.responsibilities.add(test_responsibility)
    return obligation

@pytest.fixture
def overdue_obligation(db, test_project, test_mechanism):
    """Create and return an overdue obligation."""
    obligation = Obligation.objects.create(
        obligation_number='PCEMP-002',
        project=test_project,
        primary_environmental_mechanism=test_mechanism,
        environmental_aspect='Water',
        obligation='Overdue obligation',
        accountability='SCJV',
        responsibility='SCJV - HSSE Manager',
        project_phase='Construction',
        action_due_date=timezone.now().date() - timedelta(days=10),
        status='in progress'
    )
    return obligation

@pytest.fixture
def test_evidence(db, test_obligation):
    """Create and return a test evidence file."""
    content = b'test content'
    test_file = SimpleUploadedFile(
        name='test_file.pdf',
        content=content,
        content_type='application/pdf'
    )
    evidence = ObligationEvidence.objects.create(
        obligation=test_obligation,
        file=test_file,
        description='Test evidence'
    )
    return evidence

# MODEL TESTS
@pytest.mark.django_db
class TestObligationModel:
    """Test the Obligation model."""

    def test_create_obligation(self, test_project, test_mechanism):
        """Test creating an obligation."""
        obligation = Obligation.objects.create(
            obligation_number='PCEMP-100',
            project=test_project,
            primary_environmental_mechanism=test_mechanism,
            environmental_aspect='Water',
            obligation='Test water quality monitoring',
            accountability='SCJV',
            responsibility='SCJV - HSSE Manager',
            project_phase='Construction'
        )
        assert isinstance(obligation, Obligation)
        assert obligation.obligation_number == 'PCEMP-100'
        assert obligation.status == 'not started'  # Default status

    def test_str_method(self, test_obligation):
        """Test the string representation of an obligation."""
        expected_str = f'{test_obligation.obligation_number} - {test_obligation.project.name}'
        assert str(test_obligation) == expected_str

    def test_get_next_obligation_number(self, test_obligation):
        """Test generating the next sequential obligation number."""
        next_number = Obligation.get_next_obligation_number()
        assert next_number.startswith('PCEMP-')
        # Should be one more than the highest number
        assert int(next_number.split('-')[1]) > int(test_obligation.obligation_number.split('-')[1])

    def test_is_overdue_property(self, test_obligation):
        """Test the is_overdue property."""
        # Initially not overdue
        assert test_obligation.is_overdue is False

        # Set due date to past
        test_obligation.action_due_date = timezone.now().date() - timedelta(days=1)
        test_obligation.save()
        assert test_obligation.is_overdue is True

        # Set status to completed
        test_obligation.status = 'completed'
        test_obligation.save()
        assert test_obligation.is_overdue is False

    def test_calculate_next_recurring_date(self, test_obligation):
        """Test calculating the next recurring date."""
        test_obligation.recurring_obligation = True
        test_obligation.recurring_frequency = 'monthly'

        today = timezone.now().date()
        test_obligation.action_due_date = today

        next_date = test_obligation.calculate_next_recurring_date()

        # Should be a month later
        if today.month == 12:
            expected_month = 1
            expected_year = today.year + 1
        else:
            expected_month = today.month + 1
            expected_year = today.year

        assert next_date.month == expected_month
        assert next_date.year == expected_year

    def test_update_recurring_forecasted_date(self, test_obligation):
        """Test updating the recurring forecasted date."""
        # Enable recurring obligation
        test_obligation.recurring_obligation = True
        test_obligation.recurring_frequency = 'weekly'

        # Initially no forecasted date
        assert test_obligation.recurring_forcasted_date is None

        # Update should return True (indicating a change)
        assert test_obligation.update_recurring_forecasted_date() is True

        # Should now have a forecasted date
        assert test_obligation.recurring_forcasted_date is not None

        # Calculate expected date (7 days from now)
        expected_date = timezone.now().date() + timedelta(days=7)
        assert test_obligation.recurring_forcasted_date == expected_date

@pytest.mark.django_db
class TestObligationEvidenceModel:
    """Test the ObligationEvidence model."""

    def test_create_evidence(self, test_obligation):
        """Test creating an evidence file."""
        content = b'test content'
        test_file = SimpleUploadedFile(
            name='test_file.pdf',
            content=content,
            content_type='application/pdf'
        )

        evidence = ObligationEvidence.objects.create(
            obligation=test_obligation,
            file=test_file,
            description='Test evidence'
        )

        assert evidence.obligation == test_obligation
        assert 'test_file' in evidence.file.name
        assert evidence.description == 'Test evidence'

    def test_str_method(self, test_evidence):
        """Test the string representation of evidence."""
        assert str(test_evidence).startswith(f'Evidence for {test_evidence.obligation}')

    def test_file_size(self, test_evidence):
        """Test the file_size method."""
        size = test_evidence.file_size()
        assert isinstance(size, str)
        assert 'bytes' in size or 'KB' in size or 'MB' in size

# UTILITY TESTS
class TestUtilities:
    """Test utility functions."""

    @pytest.mark.parametrize(
        'obligation_data,reference_date,expected',
        [
            ({'status': 'completed', 'action_due_date': date.today() - timedelta(days=10)}, None, False),
            ({'status': 'in progress', 'action_due_date': date.today() - timedelta(days=10)}, None, True),
            ({'status': 'not started', 'action_due_date': date.today() + timedelta(days=10)}, None, False),
            ({'status': 'in progress', 'action_due_date': None}, None, False),
        ]
    )
    def test_is_obligation_overdue(self, obligation_data, reference_date, expected):
        """Test the is_obligation_overdue utility function."""
        assert is_obligation_overdue(obligation_data, reference_date) == expected

    def test_get_obligation_status(self, test_obligation, overdue_obligation):
        """Test getting the real obligation status."""
        # Regular obligation with future date
        assert get_obligation_status(test_obligation) == test_obligation.status

        # Overdue obligation
        assert get_obligation_status(overdue_obligation) == 'overdue'

        # Change test_obligation to completed
        test_obligation.status = 'completed'
        test_obligation.save()
        assert get_obligation_status(test_obligation) == 'completed'

        # Change test_obligation to upcoming (due within 14 days)
        test_obligation.status = 'in progress'
        test_obligation.action_due_date = timezone.now().date() + timedelta(days=7)
        test_obligation.save()
        assert get_obligation_status(test_obligation) == 'upcoming'

    @pytest.mark.parametrize(
        'frequency,expected',
        [
            ('daily', 'daily'),
            ('DAILY', 'daily'),
            ('Daily', 'daily'),
            ('weekly', 'weekly'),
            ('once a week', 'weekly'),
            ('monthly', 'monthly'),
            ('every month', 'monthly'),
            ('quarterly', 'quarterly'),
            ('every 3 months', 'quarterly'),
            ('biannual', 'biannual'),
            ('semi-annual', 'biannual'),
            ('twice a year', 'biannual'),
            ('annual', 'annual'),
            ('yearly', 'annual'),
            ('once a year', 'annual'),
            ('', ''),  # Empty string
            (None, ''),  # None should return empty string
        ]
    )
    def test_normalize_frequency(self, frequency, expected):
        """Test the normalize_frequency utility function."""
        assert normalize_frequency(frequency) == expected

# FORM TESTS
@pytest.mark.django_db
class TestObligationForm:
    """Test the ObligationForm."""

    def test_form_initialization(self, test_project):
        """Test form initialization with project context."""
        form = ObligationForm(project=test_project)
        assert form.fields['project'].initial == test_project
        assert form.fields['project'].widget.__class__.__name__ == 'HiddenInput'

    @pytest.mark.parametrize(
        'field,value,valid',
        [
            ('obligation_number', 'PCEMP-123', True),
            ('obligation_number', '123', True),  # Should be auto-formatted
            ('obligation_number', 'invalid-format', False),
            ('environmental_aspect', 'Air', True),
            ('environmental_aspect', 'Other', False),  # Requires custom_aspect
        ]
    )
    def test_field_validation(self, test_project, field, value, valid):
        """Test validation of individual fields."""
        form_data = {
            'project': test_project.id,
            'environmental_aspect': 'Air',
            'obligation': 'Test obligation requirement',
            'accountability': 'Perdaman',
            'responsibility': 'SCJV - Environmental Lead',
            'status': 'not started',
            'responsibilities': [],
        }

        # Override specific field
        form_data[field] = value

        # Add custom_environmental_aspect if needed
        if field == 'environmental_aspect' and value == 'Other':
            form_data['custom_environmental_aspect'] = ''  # Empty to fail validation

        form = ObligationForm(data=form_data, project=test_project)
        is_valid = form.is_valid()

        if valid:
            assert is_valid, f'Form should be valid but got errors: {form.errors}'
        else:
            assert not is_valid, 'Form should be invalid but was valid'
            assert field in form.errors, f'Expected error in field {field} but got {form.errors}'

    def test_clean_recurring_frequency(self, test_project, test_responsibility):
        """Test cleaning of recurring frequency."""
        # With recurring obligation but no frequency
        form_data = {
            'project': test_project.id,
            'environmental_aspect': 'Air',
            'obligation': 'Test obligation requirement',
            'accountability': 'Perdaman',
            'responsibility': 'SCJV - Environmental Lead',
            'status': 'not started',
            'recurring_obligation': True,
            'responsibilities': [test_responsibility.id],
        }

        form = ObligationForm(data=form_data, project=test_project)
        assert not form.is_valid()
        assert 'recurring_frequency' in form.errors

@pytest.mark.django_db
class TestEvidenceUploadForm:
    """Test the EvidenceUploadForm."""

    def test_form_valid(self):
        """Test form validation with valid data."""
        content = b'test content'
        test_file = SimpleUploadedFile(
            name='test_file.pdf',
            content=content,
            content_type='application/pdf'
        )

        form_data = {
            'description': 'Test evidence description',
        }
        form_files = {
            'file': test_file,
        }

        form = EvidenceUploadForm(data=form_data, files=form_files)
        assert form.is_valid()

    def test_file_extension_validation(self):
        """Test validation of file extensions."""
        # Test with invalid extension
        content = b'test content'
        test_file = SimpleUploadedFile(
            name='test_file.exe',
            content=content,
            content_type='application/octet-stream'
        )

        form_data = {
            'description': 'Test evidence description',
        }
        form_files = {
            'file': test_file,
        }

        form = EvidenceUploadForm(data=form_data, files=form_files)
        assert not form.is_valid()
        assert 'file' in form.errors

# VIEW TESTS
@pytest.mark.django_db
class TestObligationViews:
    """Test obligation views."""

    def test_summary_view(self, client, test_user, test_obligation, test_mechanism):
        """Test the obligation summary view."""
        client.force_login(test_user)
        url = reverse('obligations:summary') + f'?mechanism_id={test_mechanism.id}'
        response = client.get(url)

        assert response.status_code == 200
        assert 'obligations' in response.context
        assert test_obligation in response.context['obligations']

    def test_overdue_count_view(self, client, test_user, test_project, overdue_obligation):
        """Test the total overdue obligations view."""
        client.force_login(test_user)
        url = reverse('obligations:overdue') + f'?project_id={test_project.id}'
        response = client.get(url)

        assert response.status_code == 200
        # Parse JSON response
        data = json.loads(response.content)
        assert data == 1  # Should have one overdue obligation

    def test_detail_view(self, client, test_user, test_obligation):
        """Test the obligation detail view."""
        client.force_login(test_user)
        url = reverse('obligations:detail', kwargs={'obligation_number': test_obligation.obligation_number})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['obligation'] == test_obligation

    def test_create_view_get(self, client, test_user, test_project):
        """Test getting the create obligation view."""
        client.force_login(test_user)
        url = reverse('obligations:create') + f'?project_id={test_project.id}'
        response = client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context

    def test_update_view_get(self, client, test_user, test_obligation):
        """Test getting the update obligation view."""
        client.force_login(test_user)
        url = reverse('obligations:update', kwargs={'obligation_number': test_obligation.obligation_number})
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['form'].instance == test_obligation

    def test_toggle_custom_aspect_view(self, client, test_user):
        """Test the toggle custom aspect view."""
        client.force_login(test_user)
        # Test with "Other" selected
        url = reverse('obligations:toggle_custom_aspect') + '?environmental_aspect=Other'
        response = client.get(url)

        assert response.status_code == 200
        assert 'show_field' in response.context
        assert response.context['show_field'] is True

        # Test with another option selected
        url = reverse('obligations:toggle_custom_aspect') + '?environmental_aspect=Air'
        response = client.get(url)

        assert response.status_code == 200
        assert response.context['show_field'] is False

    def test_delete_view(self, client, test_admin, test_obligation):
        """Test the delete obligation view."""
        client.force_login(test_admin)
        url = reverse('obligations:delete', kwargs={'obligation_number': test_obligation.obligation_number})
        obligation_number = test_obligation.obligation_number

        # Use POST request since it's a deletion
        response = client.post(url)

        # Should return JSON
        assert response.status_code == 200

        # Obligation should be deleted
        with pytest.raises(Obligation.DoesNotExist):
            Obligation.objects.get(obligation_number=obligation_number)

# SELENIUM TESTS
@pytest.mark.selenium
class TestObligationSelenium:
    """Test obligation views with Selenium."""

    def test_obligation_list_view(self, live_server, selenium, test_user, test_obligation, test_mechanism):
        """Test viewing the obligation list."""
        # Login first
        selenium.get(f'{live_server.url}/accounts/login/')

        username_input = selenium.find_element(By.NAME, 'username')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys(test_user.username)
        password_input.send_keys('password')

        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Navigate to obligations summary
        selenium.get(f'{live_server.url}/obligations/summary/?mechanism_id={test_mechanism.id}')

        # Wait for the page to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'obligations-heading'))
        )

        # Check if obligation is in the table
        page_source = selenium.page_source
        assert test_obligation.obligation_number in page_source
        assert test_obligation.obligation[:20] in page_source  # Check for part of the obligation text

    def test_filter_obligations(self, live_server, selenium, test_user, test_obligation, test_mechanism):
        """Test filtering obligations on the summary view."""
        # Login
        selenium.get(f'{live_server.url}/accounts/login/')

        username_input = selenium.find_element(By.NAME, 'username')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys(test_user.username)
        password_input.send_keys('password')

        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Navigate to obligations summary
        selenium.get(f'{live_server.url}/obligations/summary/?mechanism_id={test_mechanism.id}')

        # Wait for the page to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.ID, 'obligations-heading'))
        )

        # Use the search filter with a unique term from our test obligation
        search_box = selenium.find_element(By.ID, 'search-box')
        unique_term = test_obligation.obligation[:10]  # Use first part of obligation text
        search_box.clear()
        search_box.send_keys(unique_term)

        # Wait for the table to update (using a timeout approach)
        try:
            WebDriverWait(selenium, 5).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'table tbody'), unique_term)
            )
            search_results_found = True
        except BaseException:
            search_results_found = False

        assert search_results_found, 'Search did not return the expected obligation'

        # Clear and try a search term that shouldn't match anything
        search_box.clear()
        search_box.send_keys('ZXY-NONEXISTENT-TERM-123456789')

        # Wait a bit for the table to update
        import time
        time.sleep(2)

        # Check if we have a "no matching obligations" message or empty table
        page_source = selenium.page_source
        no_results = 'No obligations match' in page_source or len(selenium.find_elements(By.CSS_SELECTOR, 'table tbody tr')) == 0
        assert no_results, 'Search should not find any obligations'

    def test_view_obligation_details(self, live_server, selenium, test_user, test_obligation):
        """Test viewing obligation details."""
        # Login
        selenium.get(f'{live_server.url}/accounts/login/')

        username_input = selenium.find_element(By.NAME, 'username')
        password_input = selenium.find_element(By.NAME, 'password')

        username_input.send_keys(test_user.username)
        password_input.send_keys('password')

        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Go directly to obligation detail page
        selenium.get(f'{live_server.url}/obligations/view/{test_obligation.obligation_number}/')

        # Wait for the page to load
        WebDriverWait(selenium, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'obligation-details'))
        )

        # Check that the page contains key obligation information
        page_source = selenium.page_source
        assert test_obligation.obligation_number in page_source
        assert test_obligation.obligation in page_source
        assert test_obligation.environmental_aspect in page_source
