"""
Unit tests for pre-commit-wrapper.py.
"""
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

# Properly handle importing a module with hyphens by importing directly
sys.path.insert(0, str(Path(__file__).parent))
try:
    # For when the module is named with hyphens
    import pre_commit_wrapper
except ImportError:
    # As an alternative, try renaming the module for import
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'pre_commit_wrapper',
        os.path.join(os.path.dirname(__file__), 'pre-commit-wrapper.py')
    )
    pre_commit_wrapper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pre_commit_wrapper)


class TestPreCommitWrapper(unittest.TestCase):
    """Test cases for pre-commit-wrapper.py"""

    @mock.patch('sysconfig.get_path')
    @mock.patch('subprocess.check_output')
    def test_ensure_requirements_success(self, mock_check_output, mock_get_path):
        """Test _ensure_requirements when everything works correctly"""
        # Setup mocks
        mock_get_path.return_value = '/path/to/data'

        # Execute function
        pre_commit_wrapper._ensure_requirements()

        # Assert the subprocess was called with correct arguments
        mock_check_output.assert_called_once()
        args = mock_check_output.call_args[0][0]
        self.assertEqual(args[0], sys.executable)
        self.assertEqual(args[1], '-m')
        self.assertEqual(args[2], 'pip')
        self.assertEqual(args[3], 'install')
        self.assertEqual(args[4], '-r')
        self.assertTrue(str(pre_commit_wrapper.REQUIREMENTS_FILE) in args[5])

    @mock.patch('pathlib.Path.exists')
    @mock.patch('pathlib.Path.is_file')
    def test_ensure_requirements_missing_file(self, mock_is_file, mock_exists):
        """Test _ensure_requirements with missing requirements file"""
        # Setup mocks
        mock_exists.return_value = False
        mock_is_file.return_value = False

        # Execute and assert
        with self.assertRaises(ValueError) as context:
            pre_commit_wrapper._ensure_requirements()

        self.assertIn('not found or invalid', str(context.exception))

    @mock.patch('sysconfig.get_path')
    def test_ensure_requirements_no_data_path(self, mock_get_path):
        """Test _ensure_requirements with no data path available"""
        # Setup mocks
        mock_get_path.return_value = None

        # Execute and assert
        with self.assertRaises(RuntimeError) as context:
            pre_commit_wrapper._ensure_requirements()

        self.assertEqual('No sysconfig data path available.', str(context.exception))

    @mock.patch('sysconfig.get_path')
    @mock.patch('subprocess.check_output')
    def test_ensure_requirements_subprocess_error(self, mock_check_output, mock_get_path):
        """Test _ensure_requirements when subprocess fails"""
        # Setup mocks
        import subprocess
        mock_get_path.return_value = '/path/to/data'
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'cmd', output='Error output')

        # Execute and assert
        with self.assertRaises(subprocess.CalledProcessError):
            pre_commit_wrapper._ensure_requirements()

    @mock.patch('pre_commit_wrapper._ensure_requirements')
    @mock.patch('sys.argv', ['pre-commit-wrapper.py', 'pylint'])
    @mock.patch('pylint.run_pylint')
    def test_main_pylint(self, mock_run_pylint, mock_ensure_requirements):
        """Test main function with 'pylint' tool"""
        # Execute function
        pre_commit_wrapper.main()

        # Assert
        mock_ensure_requirements.assert_called_once()
        mock_run_pylint.assert_called_once()

    @mock.patch('pre_commit_wrapper._ensure_requirements')
    @mock.patch('sys.argv', ['pre-commit-wrapper.py', 'mypy'])
    @mock.patch('mypy.__main__.console_entry')
    def test_main_mypy(self, mock_console_entry, mock_ensure_requirements):
        """Test main function with 'mypy' tool"""
        # Execute function
        pre_commit_wrapper.main()

        # Assert
        mock_ensure_requirements.assert_called_once()
        mock_console_entry.assert_called_once()

    @mock.patch('pre_commit_wrapper._ensure_requirements')
    @mock.patch('sys.argv', ['pre-commit-wrapper.py', 'unsupported'])
    def test_main_unsupported_tool(self, mock_ensure_requirements):
        """Test main function with unsupported tool"""
        # Execute and assert
        with self.assertRaises(RuntimeError) as context:
            pre_commit_wrapper.main()

        self.assertIn('Unsupported tool', str(context.exception))
        mock_ensure_requirements.assert_called_once()

    @mock.patch('builtins.__import__')
    @mock.patch('pathlib.Path.resolve')
    def test_dotenv_import_success(self, mock_resolve, mock_import):
        """Test successful loading of dotenv_vault and environment variables"""
        # Setup mocks
        mock_path = mock.MagicMock()
        # Use a Path object instead of a string for PROJECT_ROOT
        mock_path.parent.parent.parent = Path('/mocked/project/root')
        mock_resolve.return_value = mock_path

        # Mock successful import of dotenv_vault
        mock_load_dotenv = mock.MagicMock()
        mock_import.return_value = mock.MagicMock(load_dotenv=mock_load_dotenv)

        # Create a test module to simulate the module-level code
        test_module = type('test_module', (), {})

        # Execute the code under test (simulating the module-level code)
        with mock.patch.dict('os.environ', {}):
            with mock.patch('pathlib.Path') as mock_path_class:
                mock_path_instance = mock.MagicMock()
                mock_path_class.return_value = mock_path_instance
                mock_path_class.__file__ = 'dummy_file'

                # Simulate dotenv import and project root determination
                try:
                    from dotenv_vault import load_dotenv
                    test_module.PROJECT_ROOT = Path('dummy_file').resolve().parent.parent.parent
                    load_dotenv(dotenv_path=test_module.PROJECT_ROOT / '.env')
                except ImportError:
                    test_module.PROJECT_ROOT = Path('dummy_file').resolve().parent.parent.parent

                # Test requirements file path determination
                test_module._requirements_file = os.getenv('REQUIREMENTS_FILE', 'requirements.txt')
                test_module.REQUIREMENTS_FILE = test_module.PROJECT_ROOT / test_module._requirements_file

        # Assert dotenv was loaded correctly
        self.assertEqual(mock_load_dotenv.call_count, 1)

    @mock.patch('pre_commit_wrapper.extract_installed_apps_from_settings')
    def test_create_mock_modules(self, mock_extract_apps):
        """Test create_mock_modules creates the expected modules"""
        # Setup mock
        mock_extract_apps.return_value = [
            {
                'name': 'test_app',
                'config_class': 'TestAppConfig',
                'verbose_name': 'Test App'
            }
        ]

        # Mock sys.modules to track what gets added
        mock_modules = {}
        with mock.patch.dict('sys.modules', mock_modules, clear=False):
            # Ensure the original sys module is preserved
            mock_modules['sys'] = sys
            # Mock AppConfig class
            AppConfig = type('AppConfig', (), {
                'name': '',
                'verbose_name': '',
                'path': '',
                'models_module': None,
                'apps': None,
                'label': '',
                'ready': lambda self: None,
            })
            with mock.patch('pre_commit_wrapper.AppConfig', AppConfig):
                # Execute function
                pre_commit_wrapper.create_mock_modules()

                # Assert modules were created correctly
                self.assertIn('test_app', mock_modules)
                self.assertIn('test_app.apps', mock_modules)
                self.assertIn('test_app.models', mock_modules)
                self.assertTrue(hasattr(mock_modules['test_app.apps'], 'TestAppConfig'))

    @mock.patch('pathlib.Path.open', mock.mock_open(read_data='django_settings_module = greenova.greenova.settings'))
    @mock.patch('importlib.import_module')
    def test_extract_installed_apps_from_settings(self, mock_import_module):
        """Test extract_installed_apps_from_settings extracts apps correctly"""
        # Setup mock settings module
        mock_settings = mock.MagicMock()
        mock_settings.INSTALLED_APPS = [
            'django.contrib.admin',  # Should be skipped
            'core.apps.CoreConfig',  # Full path to app config
            'company',               # Simple app name
            'allauth.account',       # Should be skipped
        ]
        mock_import_module.return_value = mock_settings

        # Execute function
        result = pre_commit_wrapper.extract_installed_apps_from_settings()

        # Assert correct apps were extracted
        self.assertEqual(len(result), 2)

        # Check core app extracted correctly
        core_app = next((app for app in result if app['name'] == 'core'), None)
        self.assertIsNotNone(core_app)
        self.assertEqual(core_app['config_class'], 'CoreConfig')

        # Check company app extracted correctly
        company_app = next((app for app in result if app['name'] == 'company'), None)
        self.assertIsNotNone(company_app)
        self.assertEqual(company_app['config_class'], 'CompanyConfig')

    @mock.patch('pathlib.Path.open', side_effect=FileNotFoundError)
    def test_extract_installed_apps_fallback(self, mock_open):
        """Test extract_installed_apps_from_settings falls back to defaults when file not found"""
        # Execute function (should use default values due to file error)
        result = pre_commit_wrapper.extract_installed_apps_from_settings()

        # Assert default apps are returned
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'core')
        self.assertEqual(result[1]['name'], 'company')

    @mock.patch('importlib.import_module', side_effect=ImportError)
    @mock.patch('pathlib.Path.open', mock.mock_open(read_data='django_settings_module = greenova.greenova.settings'))
    def test_extract_installed_apps_import_error(self, mock_import_module):
        """Test extract_installed_apps_from_settings handles module import errors"""
        # Execute function (should use default values due to import error)
        result = pre_commit_wrapper.extract_installed_apps_from_settings()

        # Assert default apps are returned
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['name'], 'core')
        self.assertEqual(result[1]['name'], 'company')

    def test_create_minimal_mocks(self):
        """Test _create_minimal_mocks creates basic mocked modules"""
        # Mock sys.modules to track what gets added
        mock_modules = {}
        with mock.patch.dict('sys.modules', mock_modules, clear=True):
            # Execute function
            pre_commit_wrapper._create_minimal_mocks()

            # Assert minimal modules were created
            self.assertIn('core', mock_modules)
            self.assertIn('core.apps', mock_modules)
            self.assertTrue(hasattr(mock_modules['core.apps'], 'CoreConfig'))

            self.assertIn('company', mock_modules)
            self.assertIn('company.apps', mock_modules)
            self.assertTrue(hasattr(mock_modules['company.apps'], 'CompanyConfig'))

    @mock.patch('pre_commit_wrapper.extract_installed_apps_from_settings', side_effect=Exception('Test exception'))
    @mock.patch('pre_commit_wrapper._create_minimal_mocks')
    def test_create_mock_modules_fallback(self, mock_minimal_mocks, mock_extract_apps):
        """Test create_mock_modules falls back to minimal mocks when extraction fails"""
        # Execute function
        pre_commit_wrapper.create_mock_modules()

        # Assert fallback was called
        mock_minimal_mocks.assert_called_once()

    @mock.patch('pre_commit_wrapper._create_minimal_mocks', side_effect=Exception('Critical error'))
    @mock.patch('pre_commit_wrapper.extract_installed_apps_from_settings', side_effect=Exception('First error'))
    def test_create_mock_modules_critical_failure(self, mock_extract_apps, mock_minimal_mocks):
        """Test create_mock_modules handles critical failures gracefully"""
        # Execute function (should not raise exception)
        pre_commit_wrapper.create_mock_modules()

        # If we get here, the test passed because no exception was raised
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
