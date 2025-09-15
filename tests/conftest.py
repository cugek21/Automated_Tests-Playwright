"""
conftest.py

Fixtures and configuration for Playwright-based automated tests.
Provides browser, viewport, context, and utility fixtures for consistent test setup.

Author: Radek Jíša
Email: radek.jisa@gmail.com
"""

import os
import logging

import pytest
from playwright.sync_api import sync_playwright, Page

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('test.log', mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

URL = 'https://engeto.cz/'

TIMEOUT = 0.5  # seconds, used for response time tests

BLOCKED_DOMAINS = [
            'facebook.com', 
            'youtube.com', 
            'instagram.com', 
            'linkedin.com', 
            'discord.gg'
            ]

VIEWPORTS = [
    {'width': 375, 'height': 667},     # small phone
    {'width': 390, 'height': 884},     # medium phone
    {'width': 430, 'height': 932},     # large phone
    {'width': 768, 'height': 1024},    # small tablet
    {'width': 820, 'height': 1180},    # medium tablet
    {'width': 1024, 'height': 1366},   # large tablet
]

@pytest.fixture(params=['chromium', 'firefox', 'webkit'])
def browser_type(request: pytest.FixtureRequest) -> str:
    """
    Provides a browser type for testing: 'chromium', 'firefox', or 'webkit'.

    Args:
        request (pytest.FixtureRequest): Used to access the current browser type.

    Returns:
        str: The selected browser type for the test.
    """
    return request.param

@pytest.fixture(params=VIEWPORTS)
def viewport(request: pytest.FixtureRequest) -> dict[str, int]:
    """
    Provides a viewport size for testing from the VIEWPORTS list.

    Args:
        request (pytest.FixtureRequest): Used to access the current viewport parameter.

    Returns:
        Any: The selected viewport size for the test.
    """
    return request.param

@pytest.fixture()
def get_context_options(viewport: dict[str, int], browser_type: str) -> dict[str, object]:
    """
    Generates browser context options for testing, customized by viewport and browser type.

    Args:
        viewport (dict[str, int]): The viewport size for the test.
        browser_type (str): The browser type ('chromium', 'firefox', or 'webkit').

    Returns:
        dict[str, object]: Options for configuring the browser context.
    """
    options = {
        'viewport': viewport,
        'user_agent': (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 '
            'Mobile/15E148 Safari/604.1'
        ),
        'device_scale_factor': 2,
        'has_touch': True,
    }
    if browser_type != 'firefox':
        options['is_mobile'] = True
    return options

@pytest.fixture()
def page(browser_type: str, get_context_options: dict[str, object]) -> Page:
    """
    Provides a Playwright page object configured with the specified browser and context options.

    Args:
        browser_type (str): The browser type to launch ('chromium', 'firefox', or 'webkit').
        get_context_options (dict): Options for configuring the browser context.

    Yields:
        playwright.sync_api.Page: The opened page for testing.
    """
    headless_env = os.getenv('HEADLESS', 'true').lower()
    headless = headless_env == 'true'

    with sync_playwright() as p:
        logger.info('Launching browser: %s, headless=%s', browser_type, headless)
        browser = getattr(p, browser_type).launch(headless=headless)
        logger.info('Creating browser context with options: %s', get_context_options)
        context = browser.new_context(**get_context_options)
        logger.debug('Opening new page')
        page = context.new_page()
        yield page
        logger.info('Closing browser')
        browser.close()

@pytest.fixture()
def refuse_cookies(page: Page) -> None:
    """
    Provides a callable that clicks the cookie refusal button on the page if it is visible.

    Args:
        page (Page): The Playwright page object to interact with.

    Returns:
        Callable[[], None]: A function that refuses cookies when called.
    """
    def _refuse():
        refuse_button = page.locator('#cookiescript_reject')
        if refuse_button.is_visible():
            logger.debug('Refusing cookies by clicking #cookiescript_reject')
            refuse_button.click()
        else:
            logger.warning('No cookie refusal button visible.')
    return _refuse
