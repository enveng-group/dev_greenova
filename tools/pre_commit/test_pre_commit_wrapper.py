"""
Unit tests for pre-commit-wrapper.py using pytest.
"""
import os
import sys
from pathlib import Path

import pytest

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


class TestPreCommitWrapper:
    """Test cases for pre-commit-wrapper.py"""

    @pytest.fixture
    def mock_env(self, monkeypatch):
        """Set up environment variables for testing."""
        monkeypatch.setattr(sys, 'argv', ['pre-commit-wrapper.py', 'pylint'])
        return monkeypatch

    def test_ensure_requirements_success(self, mocker):
        """Test _ensure_requirements when everything works correctly"""
        # Setup mocks
        mock_get_path = mocker.patch('sysconfig.get_path')
        mock_get_path.return_value = '/path/to/data'
        mock_check_output = mocker.patch('subprocess.check_output')

        # Execute function
        pre_commit_wrapper._ensure_requirements()

        # Assert the subprocess was called with correct arguments
        mock_check_output.assert_called_once()
        args = mock_check_output.call_args[0][0]
        assert args[0] == sys.executable
        assert args[1] == '-m'
        assert args[2] == 'pip'
        assert args[3] == 'install'
        assert args[4] == '-r'
        assert str(pre_commit_wrapper.REQUIREMENTS_FILE) in args[5]

    def test_ensure_requirements_missing_file(self, mocker):
        """Test _ensure_requirements with missing requirements file"""
        # Setup mocks
        mock_exists = mocker.patch('pathlib.Path.exists')
        mock_exists.return_value = False
        mock_is_file = mocker.patch('pathlib.Path.is_file')
        mock_is_file.return_value = False

        # Execute and assert
        with pytest.raises(ValueError, match='not found or invalid'):
            pre_commit_wrapper._ensure_requirements()

    def test_ensure_requirements_no_data_path(self, mocker):
        """Test _ensure_requirements with no data path available"""
        # Setup mocks
        mock_get_path = mocker.patch('sysconfig.get_path')
        mock_get_path.return_value = None

        # Execute and assert
        with pytest.raises(RuntimeError, match='No sysconfig data path available.'):
            pre_commit_wrapper._ensure_requirements()

    def test_ensure_requirements_subprocess_error(self, mocker):
        """Test _ensure_requirements when subprocess fails"""
        # Setup mocks
        import subprocess
        mock_get_path = mocker.patch('sysconfig.get_path')
        mock_get_path.return_value = '/path/to/data'
        mock_check_output = mocker.patch('subprocess.check_output')
        mock_check_output.side_effect = subprocess.CalledProcessError(1, 'cmd', output='Error output')

        # Execute and assert
        with pytest.raises(subprocess.CalledProcessError):
            pre_commit_wrapper._ensure_requirements()

    def test_main_pylint(self, mocker, mock_env):
        """Test main function with 'pylint' tool"""
        # Setup mocks
        mock_ensure_reqs = mocker.patch('pre_commit_wrapper._ensure_requirements')
        mock_run_pylint = mocker.patch('pylint.run_pylint')

        # Execute function
        pre_commit_wrapper.main()

        # Assert
        mock_ensure_reqs.assert_called_once()
        mock_run_pylint.assert_called_once()

    def test_main_mypy(self, mocker):
        """Test main function with 'mypy' tool"""
        # Setup mocks
        mocker.patch.object(sys, 'argv', ['pre-commit-wrapper.py', 'mypy'])
        mock_ensure_reqs = mocker.patch('pre_commit_wrapper._ensure_requirements')
        mock_console_entry = mocker.patch('mypy.__main__.console_entry')

        # Execute function
        pre_commit_wrapper.main()

        # Assert
        mock_ensure_reqs.assert_called_once()
        mock_console_entry.assert_called_once()

    def test_main_unsupported_tool(self, mocker):
        """Test main function with unsupported tool"""
        # Setup mocks
        mocker.patch.object(sys, 'argv', ['pre-commit-wrapper.py', 'unsupported'])
        mock_ensure_reqs = mocker.patch('pre_commit_wrapper._ensure_requirements')

        # Execute and assert
        with pytest.raises(RuntimeError, match='Unsupported tool'):
            pre_commit_wrapper.main()

        mock_ensure_reqs.assert_called_once()

    def test_extract_installed_apps_from_settings(self, mocker):
        """Test extract_installed_apps_from_settings extracts apps correctly"""
        # Setup mock settings module
        mock_open = mocker.patch('pathlib.Path.open', mocker.mock_open(
            read_data='django_settings_module = greenova.settings'
        ))
        mock_import_module = mocker.patch('importlib.import_module')
        mock_settings = mocker.MagicMock()
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
        assert len(result) == 2

        # Check core app extracted correctly
        core_app = next((app for app in result if app['name'] == 'core'), None)
        assert core_app is not None
        assert core_app['config_class'] == 'CoreConfig'

        # Check company app extracted correctly
        company_app = next((app for app in result if app['name'] == 'company'), None)
        assert company_app is not None
        assert company_app['config_class'] == 'CompanyConfig'

    def test_extract_installed_apps_fallback(self, mocker):
        """Test extract_installed_apps_from_settings falls back to defaults when file not found"""
        # Setup mock
        mock_open = mocker.patch('pathlib.Path.open', side_effect=FileNotFoundError)

        # Execute function (should use default values due to file error)
        result = pre_commit_wrapper.extract_installed_apps_from_settings()

        # Assert default apps are returned
        assert len(result) == 2
        assert result[0]['name'] == 'core'
        assert result[1]['name'] == 'company'

    def test_extract_installed_apps_import_error(self, mocker):
        """Test extract_installed_apps_from_settings handles module import errors"""
        # Setup mocks
        mock_open = mocker.patch('pathlib.Path.open', mocker.mock_open(
            read_data='django_settings_module = greenova.settings'
        ))
        mock_import_module = mocker.patch('importlib.import_module', side_effect=ImportError)

        # Execute function (should use default values due to import error)
        result = pre_commit_wrapper.extract_installed_apps_from_settings()

        # Assert default apps are returned
        assert len(result) == 2
        assert result[0]['name'] == 'core'
        assert result[1]['name'] == 'company'

    def test_create_mock_modules_fallback(self, mocker):
        """Test create_mock_modules falls back to minimal mocks when extraction fails"""
        # Setup mocks
        mock_extract = mocker.patch(
            'pre_commit_wrapper.extract_installed_apps_from_settings',
            side_effect=Exception('Test exception')
        )
        mock_minimal = mocker.patch('pre_commit_wrapper._create_minimal_mocks')

        # Execute function
        pre_commit_wrapper.create_mock_modules()

        # Assert fallback was called
        mock_minimal.assert_called_once()

    def test_create_mock_modules_critical_failure(self, mocker):
        """Test create_mock_modules handles critical failures gracefully"""
        # Setup mocks
        mock_extract = mocker.patch(
            'pre_commit_wrapper.extract_installed_apps_from_settings',
            side_effect=Exception('First error')
        )
        mock_minimal = mocker.patch(
            'pre_commit_wrapper._create_minimal_mocks',
            side_effect=Exception('Critical error')
        )

        # Execute function (should not raise exception)
        pre_commit_wrapper.create_mock_modules()

        # If we get here, the test passed because no exception was raised
        assert True
