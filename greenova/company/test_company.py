import os
import tempfile

import pytest
from company.models import Company, CompanyDocument, CompanyMembership
from company.views import is_company_admin
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test.client import RequestFactory
from django.urls import reverse
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

User = get_user_model()

# ----- FIXTURES -----

@pytest.fixture
def test_image():
    """Fixture to create a test image file."""
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as img:
        img.write(b'dummy image content')
        img_path = img.name

    yield img_path
    os.unlink(img_path)  # Delete the file after test

@pytest.fixture
def test_document():
    """Fixture to create a test document file."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as doc:
        doc.write(b'dummy pdf content')
        doc_path = doc.name

    yield doc_path
    os.unlink(doc_path)  # Delete the file after test

@pytest.fixture
def test_company(db):
    """Create a test company."""
    return Company.objects.create(
        name='Test Company',
        description='A company for testing',
        company_type='client',
        industry='manufacturing',
        is_active=True
    )

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
        'company_owner': django_user_model.objects.create_user(
            'owner', 'owner@example.com', 'ownerpassword', is_active=True
        ),
        'company_admin': django_user_model.objects.create_user(
            'companyadmin', 'admin@company.com', 'adminpassword', is_active=True
        ),
        'company_manager': django_user_model.objects.create_user(
            'manager', 'manager@company.com', 'managerpassword', is_active=True
        ),
        'company_member': django_user_model.objects.create_user(
            'member', 'member@company.com', 'memberpassword', is_active=True
        ),
    }
    return users

@pytest.fixture
def company_with_members(db, test_company, test_users):
    """Create a test company with members in different roles."""
    # Add members to company with different roles
    CompanyMembership.objects.create(
        company=test_company, user=test_users['company_owner'], role='owner', is_primary=True
    )
    CompanyMembership.objects.create(
        company=test_company, user=test_users['company_admin'], role='admin', is_primary=True
    )
    CompanyMembership.objects.create(
        company=test_company, user=test_users['company_manager'], role='manager', is_primary=True
    )
    CompanyMembership.objects.create(
        company=test_company, user=test_users['company_member'], role='member', is_primary=True
    )

    return test_company

@pytest.fixture
def authenticated_client(client, test_users, request):
    """Return an authenticated client for a specified user role."""
    user_role = request.param
    user = test_users[user_role]
    client.force_login(user)
    return client


# ----- MODEL TESTS -----

@pytest.mark.django_db
class TestCompanyModels:
    """Test company models functionality."""

    def test_company_creation(self, test_company):
        """Test company model creation."""
        assert test_company.name == 'Test Company'
        assert test_company.company_type == 'client'
        assert test_company.is_active is True

    def test_company_str_representation(self, test_company):
        """Test the company string representation."""
        assert str(test_company) == 'Test Company'

    def test_company_methods(self, company_with_members):
        """Test company model methods."""
        # Test member count
        assert company_with_members.get_member_count() == 4

        # Test get_members_by_role
        owners = company_with_members.get_members_by_role('owner')
        assert owners.count() == 1
        assert owners.first().username == 'owner'

        # Test add_member and remove_member methods
        new_user = User.objects.create_user('newuser', 'new@example.com', 'password')
        company_with_members.add_member(new_user, 'view_only')

        assert CompanyMembership.objects.filter(company=company_with_members, user=new_user).exists()
        assert company_with_members.get_member_count() == 5

        company_with_members.remove_member(new_user)
        assert not CompanyMembership.objects.filter(company=company_with_members, user=new_user).exists()
        assert company_with_members.get_member_count() == 4

    def test_membership_primary_constraint(self, test_users):
        """Test that only one company can be primary for a user."""
        user = test_users['regular_user']

        company1 = Company.objects.create(name='Company One')
        company2 = Company.objects.create(name='Company Two')

        # Create first primary membership
        membership1 = CompanyMembership.objects.create(
            company=company1, user=user, role='member', is_primary=True
        )
        assert membership1.is_primary is True

        # Create second primary membership
        membership2 = CompanyMembership.objects.create(
            company=company2, user=user, role='member', is_primary=True
        )
        assert membership2.is_primary is True

        # First membership should no longer be primary
        membership1.refresh_from_db()
        assert membership1.is_primary is False

    def test_company_document_creation(self, test_company, test_users, test_document):
        """Test creating company documents."""
        user = test_users['company_owner']

        with open(test_document, 'rb') as f:
            document = CompanyDocument.objects.create(
                company=test_company,
                name='Test Document',
                description='A test document',
                file=SimpleUploadedFile('test.pdf', f.read()),
                document_type='report',
                uploaded_by=user
            )

        assert document.name == 'Test Document'
        assert document.company == test_company
        assert document.uploaded_by == user
        assert str(document) == 'Test Document (Test Company)'


# ----- VIEW TESTS -----

@pytest.mark.django_db
class TestCompanyViews:
    """Test company views basic functionality."""

    def test_company_list_requires_login(self, client):
        """Test company list view requires authentication."""
        url = reverse('company:list')
        response = client.get(url)

        # Should redirect to login page
        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    @pytest.mark.parametrize('authenticated_client', ['regular_user'], indirect=True)
    def test_company_list_view(self, authenticated_client, test_company):
        """Test company list view."""
        url = reverse('company:list')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert test_company.name in response.content.decode()
        assert 'Companies' in response.content.decode()

    @pytest.mark.parametrize('authenticated_client', ['regular_user'], indirect=True)
    def test_company_detail_view(self, authenticated_client, test_company):
        """Test company detail view."""
        url = reverse('company:detail', kwargs={'company_id': test_company.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert test_company.name in response.content.decode()
        assert test_company.description in response.content.decode()

    def test_company_search_functionality(self, client, test_users):
        """Test company search and filter functionality."""
        # Create test companies
        client.force_login(test_users['regular_user'])
        Company.objects.create(name='Alpha Manufacturing', company_type='client', industry='manufacturing')
        Company.objects.create(name='Beta Construction', company_type='contractor', industry='construction')
        Company.objects.create(name='Gamma Energy', company_type='consultant', industry='energy')

        # Test search by name
        url = reverse('company:list') + '?search=alpha'
        response = client.get(url)
        content = response.content.decode()
        assert 'Alpha Manufacturing' in content
        assert 'Beta Construction' not in content

        # Test filter by company_type
        url = reverse('company:list') + '?company_type=contractor'
        response = client.get(url)
        content = response.content.decode()
        assert 'Beta Construction' in content
        assert 'Alpha Manufacturing' not in content

        # Test filter by industry
        url = reverse('company:list') + '?industry=energy'
        response = client.get(url)
        content = response.content.decode()
        assert 'Gamma Energy' in content
        assert 'Alpha Manufacturing' not in content


@pytest.mark.django_db
class TestCompanyCreation:
    """Test company creation functionality."""

    def test_company_create_requires_login(self, client):
        """Test company creation requires authentication."""
        url = reverse('company:create')
        response = client.get(url)

        assert response.status_code == 302
        assert '/accounts/login/' in response['Location']

    @pytest.mark.parametrize('authenticated_client', ['superuser'], indirect=True)
    def test_company_create_view_superuser(self, authenticated_client):
        """Test company creation by superuser."""
        url = reverse('company:create')
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert 'Create Company' in response.content.decode()

        # Test form submission
        company_data = {
            'name': 'New Test Company',
            'description': 'Created in test',
            'company_type': 'client',
            'industry': 'manufacturing',
            'is_active': True,
        }

        response = authenticated_client.post(url, company_data)
        assert response.status_code == 302

        # Verify company was created
        company = Company.objects.get(name='New Test Company')
        assert company.description == 'Created in test'

        # Verify creator was added as owner
        membership = CompanyMembership.objects.get(company=company)
        assert membership.role == 'owner'
        assert membership.is_primary is True

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_company_create_by_company_admin(self, authenticated_client, company_with_members):
        """Test company creation by a company admin."""
        url = reverse('company:create')
        response = authenticated_client.get(url)

        assert response.status_code == 200

        # Test form submission
        company_data = {
            'name': 'Admin Created Company',
            'description': 'Created by admin',
            'company_type': 'consultant',
            'is_active': True,
        }

        response = authenticated_client.post(url, company_data)
        assert response.status_code == 302

        # Verify company was created
        company = Company.objects.get(name='Admin Created Company')
        assert company.description == 'Created by admin'


@pytest.mark.django_db
class TestCompanyEditing:
    """Test company editing functionality."""

    @pytest.mark.parametrize('authenticated_client', ['company_owner'], indirect=True)
    def test_company_edit_by_owner(self, authenticated_client, company_with_members):
        """Test company editing by its owner."""
        url = reverse('company:edit', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert 'Update Company' in response.content.decode()

        # Test form submission
        updated_data = {
            'name': company_with_members.name,
            'description': 'Updated description',
            'company_type': company_with_members.company_type,
            'industry': 'energy',  # Changed industry
            'is_active': company_with_members.is_active,
        }

        response = authenticated_client.post(url, updated_data)
        assert response.status_code == 302

        # Verify company was updated
        company_with_members.refresh_from_db()
        assert company_with_members.description == 'Updated description'
        assert company_with_members.industry == 'energy'

    @pytest.mark.parametrize('authenticated_client', ['company_member'], indirect=True)
    def test_company_edit_by_regular_member(self, authenticated_client, company_with_members):
        """Test company editing by regular member - should be denied."""
        url = reverse('company:edit', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)

        # Should redirect with error message
        assert response.status_code == 302
        assert reverse('company:detail', kwargs={'company_id': company_with_members.id}) in response['Location']


@pytest.mark.django_db
class TestCompanyDeletion:
    """Test company deletion functionality."""

    @pytest.mark.parametrize('authenticated_client', ['company_owner'], indirect=True)
    def test_company_delete_by_owner(self, authenticated_client, company_with_members):
        """Test company deletion by its owner."""
        url = reverse('company:delete', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        assert 'Delete Company' in response.content.decode()

        # Test form submission
        response = authenticated_client.post(url)
        assert response.status_code == 302
        assert reverse('company:list') in response['Location']

        # Verify company was deleted
        assert not Company.objects.filter(id=company_with_members.id).exists()

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_company_delete_by_admin(self, authenticated_client, company_with_members):
        """Test company deletion by admin - should be denied."""
        url = reverse('company:delete', kwargs={'company_id': company_with_members.id})

        # Non-owner admin can view delete page
        response = authenticated_client.get(url)
        assert response.status_code == 200

        # But cannot delete
        response = authenticated_client.post(url)
        assert response.status_code == 302

        # Verify company still exists
        assert Company.objects.filter(id=company_with_members.id).exists()


# ----- MEMBER MANAGEMENT TESTS -----

@pytest.mark.django_db
class TestCompanyMemberManagement:
    """Test company member management functionality."""

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_manage_members_view(self, authenticated_client, company_with_members):
        """Test the manage members view."""
        url = reverse('company:members', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)

        assert response.status_code == 200
        content = response.content.decode()
        assert 'Manage Members' in content
        assert 'owner' in content
        assert 'admin' in content
        assert 'manager' in content
        assert 'member' in content

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_add_member(self, authenticated_client, company_with_members, test_users):
        """Test adding a member to a company."""
        url = reverse('company:add_member', kwargs={'company_id': company_with_members.id})
        new_user = test_users['regular_user']

        data = {
            'user': new_user.id,
            'role': 'view_only',
            'department': 'Testing',
            'position': 'Tester',
            'is_primary': True
        }

        response = authenticated_client.post(url, data)
        assert response.status_code == 200

        # Verify membership was created
        membership = CompanyMembership.objects.get(company=company_with_members, user=new_user)
        assert membership.role == 'view_only'
        assert membership.department == 'Testing'
        assert membership.is_primary is True

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_update_member_role(self, authenticated_client, company_with_members):
        """Test updating a member's role."""
        # Get the member to update
        membership = CompanyMembership.objects.get(
            company=company_with_members,
            user__username='member'
        )

        url = reverse('company:update_role', kwargs={
            'company_id': company_with_members.id,
            'member_id': membership.id
        })

        # First get the form
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert 'Update Role' in response.content.decode()

        # Then update the role
        data = {
            'role': 'manager',
            'department': 'Promoted Department',
            'position': 'Senior Tester',
            'is_primary': True
        }

        response = authenticated_client.post(url, data)
        assert response.status_code == 200

        # Verify membership was updated
        membership.refresh_from_db()
        assert membership.role == 'manager'
        assert membership.department == 'Promoted Department'

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_remove_member(self, authenticated_client, company_with_members):
        """Test removing a member from a company."""
        # Get the member to remove
        membership = CompanyMembership.objects.get(
            company=company_with_members,
            user__username='member'
        )

        url = reverse('company:remove_member', kwargs={
            'company_id': company_with_members.id,
            'member_id': membership.id
        })

        response = authenticated_client.post(url)
        assert response.status_code == 200

        # Verify membership was removed
        assert not CompanyMembership.objects.filter(id=membership.id).exists()


# ----- DOCUMENT MANAGEMENT TESTS -----

@pytest.mark.django_db
class TestCompanyDocumentManagement:
    """Test company document management functionality."""

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_upload_document(self, authenticated_client, company_with_members, test_document):
        """Test uploading a document to a company."""
        url = reverse('company:upload_document', kwargs={'company_id': company_with_members.id})

        # First get the form
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert 'Upload Document' in response.content.decode()

        # Then upload a document
        with open(test_document, 'rb') as doc_file:
            data = {
                'name': 'Test Report',
                'description': 'A test report document',
                'document_type': 'report',
                'file': SimpleUploadedFile('test.pdf', doc_file.read())
            }

            response = authenticated_client.post(url, data)

        assert response.status_code == 200

        # Verify document was created
        assert CompanyDocument.objects.filter(
            company=company_with_members,
            name='Test Report'
        ).exists()

    @pytest.mark.parametrize('authenticated_client', ['company_admin'], indirect=True)
    def test_delete_document(self, authenticated_client, company_with_members, test_document, test_users):
        """Test deleting a document from a company."""
        # First create a document
        with open(test_document, 'rb') as doc_file:
            document = CompanyDocument.objects.create(
                company=company_with_members,
                name='Document to Delete',
                file=SimpleUploadedFile('delete.pdf', doc_file.read()),
                uploaded_by=test_users['company_admin']
            )

        url = reverse('company:delete_document', kwargs={
            'company_id': company_with_members.id,
            'document_id': document.id
        })

        # First get the confirmation page
        response = authenticated_client.get(url)
        assert response.status_code == 200
        assert 'You are about to delete the document' in response.content.decode()

        # Then delete the document
        response = authenticated_client.post(url)
        assert response.status_code == 200

        # Verify document was deleted
        assert not CompanyDocument.objects.filter(id=document.id).exists()


# ----- PERMISSION TESTS -----

@pytest.mark.django_db
class TestCompanyPermissions:
    """Test company permission checks."""

    def test_is_company_admin_function(self, test_users, company_with_members):
        """Test the is_company_admin permission check function."""
        # Setup request factory
        factory = RequestFactory()

        # Test with superuser
        superuser = test_users['superuser']
        assert is_company_admin(superuser) is True

        # Test with company owner
        owner = test_users['company_owner']
        assert is_company_admin(owner) is True

        # Test with company admin
        admin = test_users['company_admin']
        assert is_company_admin(admin) is True

        # Test with company manager (not an admin)
        manager = test_users['company_manager']
        assert is_company_admin(manager) is False

        # Test with unauthenticated user
        assert is_company_admin(None) is False

    @pytest.mark.parametrize('authenticated_client', ['company_member'], indirect=True)
    def test_member_permissions(self, authenticated_client, company_with_members):
        """Test regular member permissions."""
        # Members can view company details
        url = reverse('company:detail', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)
        assert response.status_code == 200

        # Members can't edit company
        url = reverse('company:edit', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)
        assert response.status_code == 302  # Redirect with error

        # Members can't manage members
        url = reverse('company:members', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)
        assert response.status_code == 302  # Redirect with error

        # Members can't upload documents
        url = reverse('company:upload_document', kwargs={'company_id': company_with_members.id})
        response = authenticated_client.get(url)
        assert response.status_code == 302  # Redirect with error


# ----- UI TESTS WITH SELENIUM -----

@pytest.mark.django_db
class TestCompanyUI:
    """Test company UI with Selenium."""

    def test_company_list_ui(self, live_server, selenium, test_users, test_company):
        """Test company list UI and basic interactions."""
        # Login first
        selenium.get(f'{live_server.url}/accounts/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpassword')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for login to complete and redirect
        WebDriverWait(selenium, 10).until(
            lambda driver: '/dashboard/' in driver.current_url
        )

        # Visit the company list page
        selenium.get(f'{live_server.url}/company/')

        # Check page title and company list
        assert 'Companies' in selenium.title

        # Check company table headers
        headers = selenium.find_elements(By.CSS_SELECTOR, 'table th')
        header_texts = [h.text for h in headers]
        assert 'Name' in header_texts
        assert 'Type' in header_texts
        assert 'Industry' in header_texts

        # Check company entry
        company_rows = selenium.find_elements(By.CSS_SELECTOR, 'table tbody tr')
        assert len(company_rows) >= 1

        # Check company search box
        search_box = selenium.find_element(By.NAME, 'search')
        assert search_box.is_displayed()

        # Test search functionality
        search_box.send_keys('Test Company')

        # Wait for search results (HTMX refreshes the table)
        try:
            WebDriverWait(selenium, 5).until(
                EC.text_to_be_present_in_element((By.CSS_SELECTOR, 'table tbody'), 'Test Company')
            )
        except TimeoutException:
            # If the wait fails, the table may have already contained "Test Company"
            assert 'Test Company' in selenium.find_element(By.CSS_SELECTOR, 'table tbody').text

    def test_company_detail_ui(self, live_server, selenium, company_with_members):
        """Test company detail UI."""
        # Login as company owner
        selenium.get(f'{live_server.url}/accounts/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys('owner')
        password_input.send_keys('ownerpassword')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for login to complete
        WebDriverWait(selenium, 10).until(
            lambda driver: '/dashboard/' in driver.current_url
        )

        # Visit company detail page
        selenium.get(f'{live_server.url}/company/{company_with_members.id}/')

        # Check page content
        assert company_with_members.name in selenium.title

        # Check sections
        sections = selenium.find_elements(By.TAG_NAME, 'section')
        section_ids = [s.get_attribute('class') for s in sections]
        assert 'company-profile' in section_ids
        assert 'company-members' in section_ids
        assert 'company-documents' in section_ids

        # Check edit button (owner should see it)
        edit_buttons = selenium.find_elements(By.LINK_TEXT, 'Edit')
        assert len(edit_buttons) > 0
        assert edit_buttons[0].is_displayed()

    def test_company_create_form_ui(self, live_server, selenium, test_users):
        """Test company creation form UI."""
        # Login as admin
        selenium.get(f'{live_server.url}/accounts/login/')
        username_input = selenium.find_element(By.NAME, 'login')
        password_input = selenium.find_element(By.NAME, 'password')
        username_input.send_keys('admin')
        password_input.send_keys('adminpassword')
        selenium.find_element(By.XPATH, "//button[@type='submit']").click()

        # Wait for login to complete
        WebDriverWait(selenium, 10).until(
            lambda driver: '/dashboard/' in driver.current_url
        )

        # Visit company create page
        selenium.get(f'{live_server.url}/company/create/')

        # Check form fields
        assert 'Create Company' in selenium.title

        name_input = selenium.find_element(By.NAME, 'name')
        description_input = selenium.find_element(By.NAME, 'description')
        company_type_select = selenium.find_element(By.NAME, 'company_type')
        industry_select = selenium.find_element(By.NAME, 'industry')

        # Fill out and submit form
        name_input.send_keys('Selenium Test Company')
        description_input.send_keys('Created with Selenium test')

        # Submit form
        submit_button = selenium.find_element(By.XPATH, "//button[contains(text(), 'Create Company')]")
        submit_button.click()

        # Wait for redirect to company detail page
        WebDriverWait(selenium, 10).until(
            lambda driver: '/company/' in driver.current_url and 'create' not in driver.current_url
        )

        # Verify company was created and we're on detail page
        assert 'Selenium Test Company' in selenium.page_source
