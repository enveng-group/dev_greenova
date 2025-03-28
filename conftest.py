import logging
import os
import subprocess

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.safari.options import Options as SafariOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

User = get_user_model()
logger = logging.getLogger(__name__)

def pytest_configure(config):
    """Register custom pytest markers."""
    config.addinivalue_line(
        'markers', 'selenium: mark tests that require Selenium for browser automation testing'
    )


@pytest.fixture
def admin_user():
    """Create and return a superuser."""
    return User.objects.create_superuser(
        username='admin',
        email='admin@example.com',
        password='adminpass'
    )


@pytest.fixture
def regular_user():
    """Create and return a regular user."""
    return User.objects.create_user(
        username='test',
        email='test@example.com',
        password='testpass'
    )


@pytest.fixture
def authenticated_client(regular_user):
    """Return a client that's already logged in as a regular user."""
    client = Client()
    client.login(username='test', password='testpass')
    return client


@pytest.fixture
def admin_client(admin_user):
    """Return a client that's already logged in as an admin user."""
    client = Client()
    client.login(username='admin', password='adminpass')
    return client


def is_in_devcontainer():
    """Check if we're running inside a devcontainer."""
    return os.environ.get('REMOTE_CONTAINERS') == 'true' or os.path.exists('/.dockerenv')

def get_host_ip():
    """
    Get the IP address of the host machine from inside the container.
    This is typically the gateway IP for the container.
    """
    try:
        # For Docker on macOS/Windows, the host is usually accessible at host.docker.internal
        if os.path.exists('/etc/hosts'):
            with open('/etc/hosts') as f:
                for line in f:
                    if 'host.docker.internal' in line:
                        return 'host.docker.internal'

        # Alternative method: get the default route gateway
        cmd = "ip route | grep default | awk '{print $3}'"
        host_ip = subprocess.check_output(cmd, shell=True).decode().strip()
        return host_ip
    except Exception as e:
        logger.warning(f'Could not determine host IP: {e}')
        return None

@pytest.fixture(scope='session')
def driver():
    """
    Provide a WebDriver instance for Selenium tests.
    Attempts to connect to browsers on the host system when running in a devcontainer.
    Falls back to container browsers if available.

    Returns:
        WebDriver: A configured browser instance for Selenium tests
    """
    browser_driver = None

    # Check if we should skip browser tests
    if os.environ.get('CI_SKIP_BROWSER_TESTS', '').lower() in ('true', '1', 'yes'):
        pytest.skip('Browser tests disabled via CI_SKIP_BROWSER_TESTS')

    # Check if we're in a devcontainer
    in_devcontainer = is_in_devcontainer()
    logger.info(f'Running in devcontainer: {in_devcontainer}')

    # Try to connect to host browsers if in devcontainer
    if in_devcontainer:
        host_ip = get_host_ip()
        logger.info(f'Host IP determined as: {host_ip}')

        if host_ip:
            # Try Chrome on host via ChromeDriver
            try:
                logger.info('Attempting to connect to Chrome on host...')
                options = ChromeOptions()
                options.add_argument('--headless=new')  # Force headless mode
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--window-size=1920,1080')

                # For Mac, Chrome is often available with ChromeDriver
                browser_driver = webdriver.Remote(
                    command_executor=f'http://{host_ip}:9515',
                    options=options
                )
                logger.info('Successfully connected to Chrome on host!')
                return browser_driver
            except Exception as e:
                logger.warning(f'Could not connect to Chrome on host: {e}')

            # Try Safari on Mac
            try:
                logger.info('Attempting to connect to Safari on host...')
                options = SafariOptions()
                browser_driver = webdriver.Remote(
                    command_executor=f'http://{host_ip}:4444',
                    options=options
                )
                logger.info('Successfully connected to Safari on host!')
                return browser_driver
            except Exception as e:
                logger.warning(f'Could not connect to Safari on host: {e}')

    # If we couldn't connect to host browsers, try local browsers in container
    try:
        logger.info('Setting up Chrome WebDriver in container...')
        options = ChromeOptions()

        # Always use headless mode
        logger.info('Using headless mode for Chrome')
        options.add_argument('--headless=new')

        # Basic Chrome options that work well in containers
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')

        # Reduce logging noise
        options.add_experimental_option('excludeSwitches', ['enable-logging'])

        # Install and initialize Chrome driver
        service = ChromeService(ChromeDriverManager().install())
        browser_driver = webdriver.Chrome(service=service, options=options)
        logger.info('Chrome WebDriver initialized successfully')
    except Exception as e:
        logger.warning(f'Could not initialize Chrome WebDriver: {str(e)}')

        # Try Firefox as fallback
        try:
            logger.info('Attempting to use Firefox WebDriver as fallback...')
            options = FirefoxOptions()

            # Always use headless mode
            logger.info('Using headless mode for Firefox')
            options.add_argument('--headless')

            options.add_argument('--width=1920')
            options.add_argument('--height=1080')

            service = FirefoxService(GeckoDriverManager().install())
            browser_driver = webdriver.Firefox(service=service, options=options)
            logger.info('Firefox WebDriver initialized successfully')
        except Exception as firefox_error:
            logger.error(f'Firefox WebDriver also failed: {str(firefox_error)}')
            pytest.skip('Could not initialize any WebDriver. Skipping Selenium tests.')

    # If driver was created successfully, use it for tests
    if browser_driver:
        # Set implicit wait to avoid immediate failures on slow elements
        browser_driver.implicitly_wait(10)

        # Make it available in pytest config for checks in pytest_runtest_setup
        pytest.browser_driver = browser_driver

        yield browser_driver

        # Quit driver after tests
        try:
            browser_driver.quit()
        except Exception as e:
            logger.warning(f'Error quitting WebDriver: {str(e)}')
    else:
        pytest.skip('WebDriver initialization failed. Skipping Selenium tests.')


@pytest.fixture
def selenium(driver):
    """Fixture for Selenium WebDriver."""
    return driver


def pytest_runtest_setup(item):
    """Skip selenium tests if the driver fixture isn't available."""
    if 'selenium' in item.keywords and not hasattr(pytest, 'browser_driver'):
        pytest.skip('Selenium tests skipped - webdriver not available')
