"""
test_indentation_mob.py: Project 6 - Tester with Python

author: Radek Jíša
email: radek.jisa@gmail.com
"""

import pytest
from playwright.sync_api import sync_playwright, Page

URL = 'https://engeto.cz/'

VIEWPORTS = [
    {'width': 375, 'height': 667},     # small phone
    {'width': 390, 'height': 884},     # medium phone
    {'width': 430, 'height': 932},     # large phone
    {'width': 768, 'height': 1024},    # small tablet – bug: shows mobile instead of desktop
    {'width': 820, 'height': 1180},    # medium tablet – bug: shows mobile instead of desktop
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
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=False, slow_mo=500)
        context = browser.new_context(**get_context_options)
        page = context.new_page()
        yield page
        browser.close()

def refuse_cookies(page: Page) -> None:
    """
    Clicks the cookie refusal button on the page if it is visible.

    Args:
        page (Page): The Playwright page object to interact with.
    """
    refuse_button = page.locator('#cookiescript_reject')
    if refuse_button.is_visible():
        refuse_button.click()

@pytest.mark.parametrize(
        ('header_sel'),
        [
            ("#logo"),
            ("main h1:has-text('Staň se novým IT talentem')"),
            ("main a:has-text('Přehled IT kurzů')"),
            ("main h2:has-text('Přečti si o IT, kariéře a trhu práce')")
        ]
        )
def test_indentation(page: Page, header_sel: str):
    """
    Verifies that a given header element is visible and properly indented
    from the left edge of the page.

    Args:
        page (Page): The Playwright page object.
        header_sel (str): CSS selector for the header element.

    Asserts:
        - The header element is visible and has a bounding box.
        - The header element is indented by at least 16 pixels.
    """
    page.goto(URL)
    refuse_cookies(page)

    header = page.locator(header_sel)
    assert header.is_visible(), 'Header is not visible.'

    header_box = header.bounding_box()
    assert header_box is not None, 'Header bounding box not found.'

    assert header_box['x'] >= 16, 'Header is not indented.'
