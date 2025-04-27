# Django Testing Guide

This guide provides an overview of testing practices for Django applications, focusing on unit tests, integration tests, and browser-based tests using Selenium.

## Table of Contents

1. [Introduction to Django Testing](#introduction-to-django-testing)
2. [Setting Up Your Testing Environment](#setting-up-your-testing-environment)
3. [Writing Unit Tests](#writing-unit-tests)
4. [Using Django's Test Client](#using-djangos-test-client)
5. [Integration Testing with Selenium](#integration-testing-with-selenium)
6. [VS Code Integration](#vs-code-integration)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

## Introduction to Django Testing

Django's testing framework builds on Python's standard `unittest` module, providing additional tools and assertions specific to web development. Testing ensures your application functions correctly and helps prevent regressions when making changes.

### Why Test?

- **Confidence**: Know your code works as expected
- **Documentation**: Tests document how code should behave
- **Regression Prevention**: Catch bugs before they reach production
- **Refactoring Enablement**: Change code with confidence

### Django's Testing Layers

1. **Unit Tests**: Test individual components in isolation
2. **Integration Tests**: Test how components work together
3. **Functional Tests**: Test the application from the user's perspective

## Setting Up Your Testing Environment

### Basic Setup

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
```

### Testing Forms

```python
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

### Testing Views

```python
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
```

### Testing API Endpoints

```python
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
```

### Testing Templates and Context

```python
def test_transaction_list_context(self):
    """Test that the transaction list view has correct context."""
    self.client.login(username='testuser', password='testpassword')
    response = self.client.get(reverse('transaction-list'))

    self.assertEqual(response.status_code, 200)
    self.assertIn('transactions', response.context)
    self.assertIn('active_transactions', response.context)
```

## Integration Testing with Selenium

Selenium allows you to automate browser interactions for end-to-end testing.

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
```

### Writing Selenium Tests

```python
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
```

### Testing User Interactions

```python
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
```

## VS Code Integration

### Setting Up VS Code for Testing

1. **Install Required Extensions**:
   - Python extension
   - Django extension
   - Test Explorer UI

2. **Configure `launch.json` for Debugging Tests**:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
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
    }
  ]
}
```

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
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
   - Type "Python: Run Tests" and select the appropriate option

2. **Via Test Explorer**:
   - Open the Test Explorer view
   - Click the Run button next to the test or test suite

3. **Via CodeLens**:
   - Look for "Run Test" and "Debug Test" links above test methods

### Debugging Tests

1. Set breakpoints by clicking in the gutter beside line numbers
2. Run the test in debug mode through Test Explorer or CodeLens
3. Use the Debug toolbar to step through code, inspect variables, etc.

## Best Practices

### Test Structure

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
   - Models: Test creation, validation, methods
   - Forms: Test validation, error messages
   - Views: Test responses, context, templates
   - URLs: Test URL resolution

2. **Use Coverage Tools**:

```bash
coverage run --source='.' manage.py test myapp
coverage report
coverage html  # For detailed HTML report
```

### Testing Tips

1. **Use Factories for Test Data**:
   - Consider using `factory_boy` for creating test objects

2. **Mock External Services**:
   - Use `unittest.mock` or `pytest-mock` to mock API calls

3. **Use Fixtures for Common Setup**:
   - Reuse common test data setup across tests

4. **Test Edge Cases**:
   - Test boundary conditions
   - Test error handling

## Troubleshooting

### Common Issues

1. **Database Errors**:
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
