<<<<<<< HEAD
# Pytest & Django Testing Guide

This guide provides an overview of testing practices for Django applications
using pytest, focusing on unit tests, integration tests, and browser-based
tests using Selenium.

## Table of Contents

1. [Introduction to pytest for Django](#introduction-to-pytest-for-django)
2. [Setting Up Your Testing Environment](#setting-up-your-testing-environment)
3. [Writing Tests with pytest](#writing-tests-with-pytest)
4. [Using the Django Test Client](#using-the-django-test-client)
=======
# Django Testing Guide

This guide provides an overview of testing practices for Django applications, focusing on unit tests, integration tests, and browser-based tests using Selenium.

## Table of Contents

1. [Introduction to Django Testing](#introduction-to-django-testing)
2. [Setting Up Your Testing Environment](#setting-up-your-testing-environment)
3. [Writing Unit Tests](#writing-unit-tests)
4. [Using Django's Test Client](#using-djangos-test-client)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
5. [Integration Testing with Selenium](#integration-testing-with-selenium)
6. [VS Code Integration](#vs-code-integration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

<<<<<<< HEAD
## Introduction to pytest for Django

Pytest is a robust Python testing framework that offers more flexibility and
features than the standard unittest module. When combined with pytest-django,
it provides powerful tools for testing Django applications with less
boilerplate code.

### Why Use pytest?

- **Simplified Syntax**: Write tests as simple functions instead of classes
- **Powerful Fixtures**: More flexible than setUp/tearDown methods
- **Parameterization**: Test multiple scenarios with a single test
- **Rich Plugin Ecosystem**: Extend testing capabilities with plugins
- **Better Assertions**: More intuitive failure messages
- **Parallel Test Execution**: Speed up your test suite

### pytest Testing Layers
=======
## Introduction to Django Testing

Django's testing framework builds on Python's standard `unittest` module, providing additional tools and assertions specific to web development. Testing ensures your application functions correctly and helps prevent regressions when making changes.

### Why Test?

- **Confidence**: Know your code works as expected
- **Documentation**: Tests document how code should behave
- **Regression Prevention**: Catch bugs before they reach production
- **Refactoring Enablement**: Change code with confidence

### Django's Testing Layers
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test how components work together
3. **Functional Tests**: Test the application from the user's perspective

## Setting Up Your Testing Environment

### Basic Setup

<<<<<<< HEAD
Install pytest and related packages:

```bash
# Install test requirements
python -m pip install pytest pytest-django pytest-dotenv selenium webdriver-manager pytest-cov

# Add to requirements.txt or pyproject.toml
# pytest==7.4.0
# pytest-django==4.5.2
# pytest-dotenv==0.5.2
# selenium==4.10.0
# webdriver-manager==3.8.6
# pytest-cov==4.1.0
```

### Configure pytest for Django

Create a `pytest.ini` file in your project root:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = greenova.settings
python_files = test_*.py
testpaths = tests
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    selenium: marks tests requiring selenium
python_classes = Test*
python_functions = test_*
```

### Configure Environment Variables

Create a `.env.test` file for test-specific environment variables:

```
DEBUG=True
DATABASE_URL=sqlite:///:memory:
SECRET_KEY=test-secret-key
```

### Create a conftest.py File

Create a `conftest.py` file in your project root for shared fixtures:

```python
import pytest
from django.contrib.auth import get_user_model

@pytest.fixture
def admin_user():
    """Create and return an admin user."""
    User = get_user_model()
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='password'
    )

@pytest.fixture
def client_user():
    """Create and return a regular user."""
    User = get_user_model()
    return User.objects.create_user(
        username='test',
        email='user@example.com',
        password='password'
    )
```

## Writing Tests with pytest

### Test Organization

Organize tests in a `tests` directory within each Django app:

```
myapp/
├── __init__.py
├── models.py
├── views.py
├── forms.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_views.py
    └── test_forms.py
```

### Basic Test Structure

```python
# myapp/tests/test_models.py
import pytest
from myapp.models import MyModel

# Mark tests that need database access
@pytest.mark.django_db
def test_model_creation():
    """Test model instance creation."""
    item = MyModel.objects.create(name="Test Item", value=10)
    assert item.name == "Test Item"
    assert item.value == 10
```

### Using Fixtures

```python
# myapp/tests/test_models.py
import pytest
from myapp.models import Transaction

# Define a fixture for this module
@pytest.fixture
def sample_transaction(admin_user):
    """Create a sample transaction for testing."""
    return Transaction.objects.create(
        user=admin_user,
        status="active",
    )

@pytest.mark.django_db
def test_transaction_creation(sample_transaction):
    """Test transaction creation using a fixture."""
    assert sample_transaction.user.username == "admin"
    assert sample_transaction.status == "active"

@pytest.mark.django_db
def test_transaction_str_method(sample_transaction):
    """Test string representation."""
    assert str(sample_transaction) == f"Transaction {sample_transaction.id}"
=======
Django automatically configures a test database when running tests. Tests are placed in a `tests.py` file within each Django app or in a `tests` package.

```python
# myapp/tests.py
from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)
```

### Test Configuration

Modify test settings in your Django settings file:

```python
# settings.py
TEST_RUNNER = 'django.test.runner.DiscoverRunner'
```

### Installing Additional Dependencies

```bash
# Install test requirements
python -m pip install selenium webdriver-manager coverage

# Add to requirements.txt or pyproject.toml
# selenium==4.10.0
# webdriver-manager==3.8.6
# coverage==7.2.7
```

## Writing Unit Tests

Django's `TestCase` class extends the `unittest.TestCase` class with additional functionality for web applications.

### Test Structure

```python
from django.test import TestCase
from myapp.models import MyModel

class MyModelTests(TestCase):
    def setUp(self):
        """Set up test data."""
        MyModel.objects.create(name="Test Item", value=10)
    
    def tearDown(self):
        """Clean up after tests (often not needed with TestCase)."""
        pass
    
    def test_model_creation(self):
        """Test model instance creation."""
        item = MyModel.objects.get(name="Test Item")
        self.assertEqual(item.value, 10)
```

### Testing Models

```python
from django.test import TestCase
from myapp.models import Transaction

class TransactionModelTests(TestCase):
    def setUp(self):
        self.transaction = Transaction.objects.create(
            user_id="user1",
            status="active",
        )
    
    def test_transaction_creation(self):
        """Test transaction creation."""
        self.assertEqual(self.transaction.user_id, "user1")
        self.assertEqual(self.transaction.status, "active")
    
    def test_transaction_str_method(self):
        """Test string representation."""
        self.assertEqual(str(self.transaction), f"Transaction {self.transaction.id}")
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Testing Forms

```python
<<<<<<< HEAD
# myapp/tests/test_forms.py
import pytest
from myapp.forms import TransactionForm

@pytest.mark.django_db
def test_valid_form():
    """Test form with valid data."""
    data = {'user_id': 'user1', 'status': 'active'}
    form = TransactionForm(data=data)
    assert form.is_valid()

@pytest.mark.django_db
def test_invalid_form():
    """Test form with invalid data."""
    data = {'user_id': '', 'status': 'active'}
    form = TransactionForm(data=data)
    assert not form.is_valid()
    assert 'user_id' in form.errors
```

### Parameterized Tests

```python
# myapp/tests/test_models.py
import pytest
from myapp.models import Transaction

@pytest.mark.django_db
@pytest.mark.parametrize(
    "status,is_active",
    [
        ("active", True),
        ("pending", True),
        ("cancelled", False),
        ("completed", False),
    ]
)
def test_transaction_active_property(admin_user, status, is_active):
    """Test the active property with different statuses."""
    transaction = Transaction.objects.create(
        user=admin_user,
        status=status
    )
    assert transaction.is_active == is_active
```

## Using the Django Test Client

The pytest-django plugin provides a `client` fixture that you can use to test
views.
=======
from django.test import TestCase
from myapp.forms import TransactionForm

class TransactionFormTests(TestCase):
    def test_valid_form(self):
        """Test form with valid data."""
        data = {'user_id': 'user1', 'status': 'active'}
        form = TransactionForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form(self):
        """Test form with invalid data."""
        data = {'user_id': '', 'status': 'active'}
        form = TransactionForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('user_id', form.errors)
```

## Using Django's Test Client

The test client simulates a web browser, allowing you to test views and templates.
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

### Testing Views

```python
<<<<<<< HEAD
# myapp/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_unauthenticated(client):
    """Test dashboard access for unauthenticated users."""
    url = reverse('dashboard')
    response = client.get(url)
    assert response.status_code == 302  # Redirect to login

@pytest.mark.django_db
def test_dashboard_authenticated(client, admin_user):
    """Test dashboard access for authenticated users."""
    url = reverse('dashboard')
    client.force_login(admin_user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'dashboard/index.html' in [t.name for t in response.templates]
    assert 'Dashboard' in response.content.decode()
=======
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class DashboardViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.url = reverse('dashboard')

    def test_dashboard_unauthenticated(self):
        """Test dashboard access for unauthenticated users."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_authenticated(self):
        """Test dashboard access for authenticated users."""
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/index.html')
        self.assertContains(response, 'Dashboard')
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Testing API Endpoints

```python
<<<<<<< HEAD
# myapp/tests/test_api.py
import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()

@pytest.mark.django_db
def test_list_transactions(api_client, admin_user):
    """Test retrieving a list of transactions."""
    # Authenticate user
    api_client.force_authenticate(user=admin_user)

    # Make request
    url = reverse('transaction-list')
    response = api_client.get(url)

    # Assert
    assert response.status_code == 200
=======
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

class TransactionAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create test user and authenticate
        
    def test_list_transactions(self):
        """Test retrieving a list of transactions."""
        url = reverse('transaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Testing Templates and Context

```python
<<<<<<< HEAD
# myapp/tests/test_views.py
import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_transaction_list_context(client, admin_user):
    """Test that the transaction list view has correct context."""
    # Log in
    client.force_login(admin_user)

    # Get the page
    response = client.get(reverse('transaction-list'))

    # Assert
    assert response.status_code == 200
    assert 'transactions' in response.context
    assert 'active_transactions' in response.context
=======
def test_transaction_list_context(self):
    """Test that the transaction list view has correct context."""
    self.client.login(username='testuser', password='testpassword')
    response = self.client.get(reverse('transaction-list'))
    
    self.assertEqual(response.status_code, 200)
    self.assertIn('transactions', response.context)
    self.assertIn('active_transactions', response.context)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

## Integration Testing with Selenium

Selenium allows you to automate browser interactions for end-to-end testing.

<<<<<<< HEAD
### Setting Up Selenium with pytest

Add these fixtures to your project's `conftest.py`:

```python
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

@pytest.fixture(scope='session')
def browser():
    """Provide a WebDriver instance for Selenium tests."""
    chrome_options = Options()
    # Run headless by default
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)

    yield driver

    # Teardown
    driver.quit()

@pytest.fixture
def selenium(browser, live_server):
    """Fixture that provides a browser and live server for testing."""
    yield browser
    # Reset browser state between tests
    browser.delete_all_cookies()
=======
### Setting Up Selenium

```python
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up headless Chrome browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(ChromeDriverManager().install())
        cls.selenium = webdriver.Chrome(service=service, options=chrome_options)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Writing Selenium Tests

```python
<<<<<<< HEAD
# myapp/tests/test_selenium.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Mark as a selenium test
@pytest.mark.selenium
@pytest.mark.django_db
def test_login_form(selenium, live_server, client_user):
    """Test the login form using Selenium."""
    # Navigate to the login page
    selenium.get(f"{live_server.url}/accounts/login/")

    # Find form elements
    username_input = selenium.find_element(By.NAME, "username")
    password_input = selenium.find_element(By.NAME, "password")
    submit_button = selenium.find_element(By.XPATH, "//button[@type='submit']")

    # Fill in the form
    username_input.send_keys("test")
    password_input.send_keys("password")

    # Submit the form
    submit_button.click()

    # Check that login was successful (wait for an element)
    WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )

    assert "Dashboard" in selenium.page_source
=======
def test_login_form(self):
    """Test the login form using Selenium."""
    # Navigate to the login page
    self.selenium.get(f"{self.live_server_url}/accounts/login/")
    
    # Find form elements
    username_input = self.selenium.find_element(By.NAME, "username")
    password_input = self.selenium.find_element(By.NAME, "password")
    submit_button = self.selenium.find_element(By.XPATH, "//button[@type='submit']")
    
    # Fill in the form
    username_input.send_keys("testuser")
    password_input.send_keys("testpassword")
    
    # Submit the form
    submit_button.click()
    
    # Check that login was successful
    self.assertIn("Dashboard", self.selenium.page_source)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Testing User Interactions

```python
<<<<<<< HEAD
# myapp/tests/test_selenium.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.selenium
@pytest.mark.django_db
def test_transaction_creation(selenium, live_server, admin_user):
    """Test creating a new transaction through the UI."""
    # Log in first
    selenium.get(f"{live_server.url}/accounts/login/")
    username_input = selenium.find_element(By.NAME, "username")
    password_input = selenium.find_element(By.NAME, "password")
    username_input.send_keys("admin")
    password_input.send_keys("password")
    selenium.find_element(By.XPATH, "//button[@type='submit']").click()

    # Wait for login to complete
    WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "dashboard"))
    )

    # Navigate to transaction creation form
    selenium.get(f"{live_server.url}/transactions/create/")

    # Fill in the form
    user_id_input = selenium.find_element(By.ID, "id_user_id")
    status_input = selenium.find_element(By.ID, "id_status")

    user_id_input.send_keys("user1")
    status_input.send_keys("active")

    # Submit the form
    selenium.find_element(By.XPATH, "//button[@type='submit']").click()

    # Verify success message (with waiting)
    success_message = WebDriverWait(selenium, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "success-message"))
    )
    assert "Transaction created successfully" in success_message.text
=======
def test_transaction_creation(self):
    """Test creating a new transaction through the UI."""
    # Log in
    self.selenium.get(f"{self.live_server_url}/accounts/login/")
    username_input = self.selenium.find_element(By.NAME, "username")
    password_input = self.selenium.find_element(By.NAME, "password")
    username_input.send_keys("testuser")
    password_input.send_keys("testpassword")
    self.selenium.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Navigate to transaction creation form
    self.selenium.get(f"{self.live_server_url}/transactions/create/")
    
    # Fill in the form
    user_id_input = self.selenium.find_element(By.ID, "id_user_id")
    status_input = self.selenium.find_element(By.ID, "id_status")
    
    user_id_input.send_keys("user1")
    status_input.send_keys("active")
    
    # Submit the form
    self.selenium.find_element(By.XPATH, "//button[@type='submit']").click()
    
    # Verify success message
    success_message = self.selenium.find_element(By.CLASS_NAME, "success-message")
    self.assertIn("Transaction created successfully", success_message.text)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

## VS Code Integration

<<<<<<< HEAD
### Setting Up VS Code for pytest

1. **Install Required Extensions**:

   - Python extension
   - Python Test Explorer for Visual Studio Code
   - Python Test Explorer

2. **Configure `settings.json` for Test Discovery**:

```json
{
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false,
  "python.testing.nosetestsEnabled": false,
  "python.testing.pytestArgs": ["."],
  "python.linting.enabled": true
}
```

3. **Configure `.vscode/launch.json` for Debugging Tests**:
=======
### Setting Up VS Code for Testing

1. **Install Required Extensions**:
   - Python extension
   - Django extension
   - Test Explorer UI

2. **Configure `launch.json` for Debugging Tests**:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

```json
{
  "version": "0.2.0",
  "configurations": [
    {
<<<<<<< HEAD
      "name": "Python: Debug Tests",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "purpose": ["debug-test"],
      "console": "integratedTerminal",
      "justMyCode": false,
      "env": {
        "PYTEST_ADDOPTS": "--no-cov"
      }
=======
      "name": "Django Tests",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/manage.py",
      "args": [
        "test",
        "${relativeFileDirname}"
      ],
      "django": true,
      "justMyCode": true
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
    }
  ]
}
```

<<<<<<< HEAD
### Running Tests in VS Code

1. **Via Command Palette**:

=======
3. **Configure `settings.json` for Test Discovery**:

```json
{
  "python.testing.pytestEnabled": false,
  "python.testing.unittestEnabled": true,
  "python.testing.nosetestsEnabled": false,
  "python.testing.unittestArgs": [
    "-v",
    "-s",
    "./",
    "-p",
    "*test*.py"
  ]
}
```

### Running Tests in VS Code

1. **Via Command Palette**:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Python: Run Tests" and select the appropriate option

2. **Via Test Explorer**:
<<<<<<< HEAD

   - Open the Test Explorer view (flask icon in sidebar)
   - Click the Run button next to the test or test suite

3. **Via Terminal**:
   - Run `pytest` for all tests
   - Run `pytest myapp/tests/test_models.py` for specific file
   - Run `pytest myapp/tests/test_models.py::test_function` for specific test
=======
   - Open the Test Explorer view
   - Click the Run button next to the test or test suite

3. **Via CodeLens**:
   - Look for "Run Test" and "Debug Test" links above test methods
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

### Debugging Tests

1. Set breakpoints by clicking in the gutter beside line numbers
<<<<<<< HEAD
2. Run the test in debug mode through Test Explorer (play with bug icon)
=======
2. Run the test in debug mode through Test Explorer or CodeLens
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
3. Use the Debug toolbar to step through code, inspect variables, etc.

## Best Practices

### Test Structure

<<<<<<< HEAD
1. **Use Small, Focused Tests**:

   - Each test should verify one specific behavior
   - Keep tests independent of each other

2. **Use Descriptive Test Names**:

   - Name tests to describe what they're testing
   - Example: `test_user_cannot_access_admin_page_without_permissions`

3. **Use Appropriate Markers**:
   - Mark slow tests with `@pytest.mark.slow`
   - Mark database tests with `@pytest.mark.django_db`
   - Create custom markers for specific test categories

### Test Coverage

1. **Aim for Comprehensive Coverage**:

=======
1. **Follow the AAA Pattern**:
   - **Arrange**: Set up test data and conditions
   - **Act**: Perform the action to test
   - **Assert**: Check that the results are as expected

2. **Keep Tests Independent**:
   - Each test should run independently of others
   - Avoid test interdependencies

3. **Use Descriptive Test Names**:
   - Name tests to describe what they're testing
   - Example: `test_user_cannot_access_admin_page_without_permissions`

### Test Coverage

1. **Aim for Comprehensive Coverage**:
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
   - Models: Test creation, validation, methods
   - Forms: Test validation, error messages
   - Views: Test responses, context, templates
   - URLs: Test URL resolution

2. **Use Coverage Tools**:

```bash
<<<<<<< HEAD
pytest --cov=myapp
pytest --cov=myapp --cov-report=html  # For detailed HTML report
=======
coverage run --source='.' manage.py test myapp
coverage report
coverage html  # For detailed HTML report
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
```

### Testing Tips

<<<<<<< HEAD
1. **Use Fixtures for Common Setup**:

   - Create fixtures in conftest.py for reusable test components
   - Use fixture scope appropriately: function, class, module, or session

2. **Mock External Services**:

   - Use `pytest-mock` for mocking
   - Example: `def test_api_call(mocker): mocker.patch('requests.get')`

3. **Use Parameterized Tests**:

   - Test multiple scenarios with `@pytest.mark.parametrize`
   - Reduces test code duplication

4. **Test Edge Cases**:
   - Test boundary conditions
   - Test error handling and exceptions with `pytest.raises`
=======
1. **Use Factories for Test Data**:
   - Consider using `factory_boy` for creating test objects

2. **Mock External Services**:
   - Use `unittest.mock` or `pytest-mock` to mock API calls

3. **Use Fixtures for Common Setup**:
   - Reuse common test data setup across tests

4. **Test Edge Cases**:
   - Test boundary conditions
   - Test error handling
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

## Troubleshooting

### Common Issues

1. **Database Errors**:
<<<<<<< HEAD

   - Issue: Tests fail with database errors
   - Solution: Make sure tests are marked with `@pytest.mark.django_db`
   - Solution: Check for isolation issues between tests

2. **Selenium WebDriver Issues**:

   - Issue: Chrome/Firefox driver not found
   - Solution: Use webdriver-manager for automatic driver installation
   - Solution: Check that browser binaries are accessible

3. **Fixture Errors**:

   - Issue: Fixture not found or wrong scope
   - Solution: Check fixture names and make sure conftest.py is in the correct
     directory
   - Solution: Check fixture dependencies

4. **Path Issues**:
   - Issue: Tests not being discovered
   - Solution: Check that files start with `test_` and functions start with
     `test_`
   - Solution: Verify directory structure and pytest configuration

### Debugging Strategies

1. **Verbose Output**:

   - Run tests with `-v` flag for more details: `pytest -v`
   - Use `-vv` for even more verbosity

2. **Display Print Statements**:

   - Run tests with `-s` flag to see print outputs: `pytest -s`

3. **Isolate Failing Tests**:

   - Run specific tests: `pytest path/to/test.py::test_name`
   - Filter by test name pattern: `pytest -k "pattern"`

4. **Debug with PDB**:
   - Insert `import pdb; pdb.set_trace()` in your code
   - Or use `pytest --pdb` to drop into debugger on failure

## Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-django Documentation](https://pytest-django.readthedocs.io/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [pytest Fixture Patterns](https://docs.pytest.org/en/latest/fixture.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
=======
   - Issue: Tests may fail due to database conflicts
   - Solution: Ensure `TEST_NAME` is set in database configuration

2. **Selenium WebDriver Issues**:
   - Issue: Chrome/Firefox driver not found
   - Solution: Use webdriver-manager to handle driver installation

3. **Form Validation Errors**:
   - Issue: Form tests failing unexpectedly
   - Solution: Check for missing required fields or invalid data formats

4. **Authentication Issues in Tests**:
   - Issue: Views requiring authentication fail
   - Solution: Ensure proper login in `setUp` or use `force_login`

### Debugging Strategies

1. **Print Debugging**:
   - Add `print()` statements to troubleshoot
   - Use `self.print_html()` in `DjangoTestCase` to see rendered HTML

2. **Increase Verbosity**:
   - Run tests with higher verbosity: `python manage.py test --verbosity=2`

3. **Isolate Failing Tests**:
   - Run specific tests: `python manage.py test myapp.tests.TestClass.test_method`

4. **Inspect the Test Database**:
   - Use `--keepdb` flag to preserve the test database between runs

## Additional Resources

- [Django Testing Documentation](https://docs.djangoproject.com/en/4.1/topics/testing/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Django Test-Driven Development Tutorial](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
