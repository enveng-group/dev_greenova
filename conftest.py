from __future__ import annotations

import logging
import os
import subprocess
import sys
from typing import Generator, Optional, TextIO, cast

import pytest
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest
from _pytest.nodes import Item
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.test import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

# Get the User model in a type-safe way
User = get_user_model()
UserModel = cast(type[AbstractUser], User)

# Setup console logger for debugging WebDriver initialization
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(cast(TextIO, sys.stdout))
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def pytest_configure(config: Config) -> None:
    """Register custom pytest markers."""
    config.addinivalue_line(
        'markers', 'selenium: mark tests that require Selenium for browser automation testing'
    )

@pytest.fixture
def admin_user() -> AbstractUser:
    """Create and return a superuser."""
    return UserModel.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass'
    )

@pytest.fixture
def regular_user() -> AbstractUser:
    """Create and return a regular user."""
    return UserModel.objects.create_user(
        username='test',
        email='test@example.com',
        password='testpass'
    )

@pytest.fixture
def authenticated_client(regular_user: AbstractUser) -> Client:
    """Return a client that's already logged in as a regular user."""
    client = Client()
    client.login(username='test', password='testpass')
    return client

@pytest.fixture
def admin_client(admin_user: AbstractUser) -> Client:
    """Return a client that's already logged in as an admin user."""
    client = Client()
    client.login(username='admin', password='adminpass')
    return client

def verify_chrome_in_container() -> bool:
    """
    Run diagnostics to verify Chrome is properly installed and can run.
    """
    chrome_path = '/usr/local/bin/chrome'
    if not os.path.exists(chrome_path):
        logger.error(f'Chrome binary not found at {chrome_path}')
        return False

    # Check if Chrome is executable
    if not os.access(chrome_path, os.X_OK):
        try:
            os.chmod(chrome_path, 0o755)
            logger.info('Fixed Chrome executable permissions')
        except Exception as e:
            logger.error(f'Could not set executable permissions: {e}')
            return False

    # Check if Chrome can run with --version flag
    try:
        result = subprocess.run(
            [chrome_path, '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        logger.info(f'Chrome version: {result.stdout.strip()}')
        return True
    except subprocess.SubprocessError as e:
        logger.error(f'Chrome cannot run: {e}')
        return False

@pytest.fixture(scope='session')
def driver() -> Generator[WebDriver | None]:
    """
    Provide a WebDriver instance for Selenium tests using the pre-installed Chrome.
    """
    chrome_path = '/usr/local/bin/chrome'
    chromedriver_path = '/usr/local/bin/chromedriver'

    # Run diagnostics to verify Chrome setup
    if not verify_chrome_in_container():
        logger.error('Chrome verification failed - skipping browser tests')
        pytest.skip('Chrome verification failed')
        # This yield None is needed to make the fixture generator work
        yield None
        return

    # Verify binary paths
    logger.info(f'Chrome path exists: {os.path.exists(chrome_path)}')
    logger.info(f'ChromeDriver path exists: {os.path.exists(chromedriver_path)}')

    # Make ChromeDriver executable if needed
    if os.path.exists(chromedriver_path) and not os.access(chromedriver_path, os.X_OK):
        logger.info('Making ChromeDriver executable')
        os.chmod(chromedriver_path, 0o755)

    try:
        logger.info('Initializing Chrome WebDriver...')
        options = ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.binary_location = chrome_path

        # Explicitly run Chrome with debugging flags to capture more info
        options.add_argument('--enable-logging')
        options.add_argument('--log-level=0')  # Most verbose

        service = ChromeService(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service, options=options)

        # Set window size explicitly
        driver.set_window_size(1920, 1080)

        # Set implicit wait
        driver.implicitly_wait(10)

        # Store driver in pytest namespace for test setup check
        pytest.browser_driver = driver

        logger.info('Chrome WebDriver initialized successfully')
        yield driver

        # Clean up browser
        driver.quit()
        logger.info('Chrome WebDriver closed')

    except Exception as e:
        logger.error(f'Failed to initialize Chrome WebDriver: {str(e)}')

        # Fall back to webdriver_manager as a last resort
        try:
            logger.info('Attempting to use webdriver_manager as fallback...')
            options = ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            # Set window size explicitly
            driver.set_window_size(1920, 1080)

            # Set implicit wait
            driver.implicitly_wait(10)

            # Store driver in pytest namespace
            pytest.browser_driver = driver

            logger.info('WebDriver initialized with webdriver_manager')
            yield driver

            driver.quit()
            logger.info('WebDriver closed')

        except Exception as e:
            logger.error(f'WebDriver manager also failed: {str(e)}')
            # Indicate that browser tests should be skipped
            yield None

@pytest.fixture
def selenium(request: FixtureRequest, driver: WebDriver | None) -> WebDriver:
    """
    Fixture for Selenium WebDriver.

    This fixture checks if the driver was successfully created and skips
    tests if not.
    """
    if driver is None:
        pytest.skip('WebDriver could not be initialized')
    return cast(WebDriver, driver)

def pytest_runtest_setup(item: Item) -> None:
    """Skip selenium tests if the driver fixture isn't available."""
    if 'selenium' in item.keywords and not hasattr(pytest, 'browser_driver'):
        pytest.skip('Selenium tests skipped - webdriver not available')
