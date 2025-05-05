# Testing Strategy for Greenova

At Greenova, we follow a comprehensive testing strategy to ensure the quality
and reliability of our Django applications. This document outlines the types of
tests we perform, the tools and frameworks we use, and our testing best
practices.

## 🧪 Types of Tests

We categorize our tests into three main types:

### Unit Tests

Unit tests are designed to test individual components or functions in
isolation. They ensure that each part of the application behaves as expected.
We write unit tests for models, forms, views, and other components. We use
Python's `unittest` framework and `pytest` for running tests.

### Integration Tests

Integration tests verify how different parts of the application work together.
This includes testing interactions between models, views, templates, and
external services. These tests ensure that the integrated components function
correctly as a group. We also test the integration of our application with
external APIs and services. We use Django's test client for simulating requests
and checking responses.

### End-to-End (E2E) Tests

End-to-End tests simulate real user scenarios, testing the application from
start to finish. These tests are usually automated and cover critical user
journeys through the application. We use tools like Selenium or Playwright to
automate browser interactions and simulate user behavior.

## 🛠️ Testing Tools and Frameworks

We use a combination of built-in and third-party tools for testing in Django:

- **Django's Test Framework**: For writing and running unit and integration
  tests.
- **Selenium**: For automating browser interactions in E2E tests.
- **pytest**: As an alternative test runner with powerful features like
  fixtures and plugins.
- **Factory_boy**: For creating test data and objects.
- **Mock**: For mocking external services and APIs.

## 🏗️ Test Structure

We follow a consistent structure for organizing our tests:

1. **Test File Naming**: Test files should be named `test_<module_name>.py`.
2. **Test Case Naming**: Test functions or methods should start with `test_`.
3. **Fixtures**: Use `pytest` fixtures for setting up test data and resources.
   Fixtures should be defined in `conftest.py` files.

### Test Structure Example

```python
# myapp/tests/test_models.py

from django.test import TestCase
from .factories import MyModelFactory

class MyModelTestCase(TestCase):
    def setUp(self):
        self.instance = MyModelFactory()

    def test_str(self):
        self.assertEqual(str(self.instance), self.instance.name)
```

## 🏁 Running Tests

To run the tests, use the following command:

```bash
python manage.py test
```

For a specific app:

```bash
python manage.py test myapp
```

For a specific test case:

```bash
python manage.py test myapp.tests.MyTestCase
```

For a specific test method:

```bash
python manage.py test myapp.tests.MyTestCase.test_method
```

## 📈 Test Coverage

We measure test coverage to ensure that our tests cover a significant portion
of the codebase. We use `coverage.py` for measuring coverage. To generate a
coverage report, run:

```bash
coverage run manage.py test
coverage report
```

For an HTML report, run:

```bash
coverage html
```

## 🧹 Cleaning Up

After running tests, you may want to clean up the database or other resources.
Use the following command to delete all data from the test database:

```bash
python manage.py flush --no-input
```

To delete the test database file (for SQLite), delete the `db.sqlite3` file in
the project root.

## 📚 Further Reading

- [Django Testing Documentation](https://docs.djangoproject.com/en/stable/topics/testing/)
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [Factory_boy Documentation](https://factoryboy.readthedocs.io/en/stable/)
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)
- [Playwright Documentation](https://playwright.dev/docs/intro)

By following this testing strategy, we ensure that our Django applications are
robust, reliable, and ready for production. Happy testing!
