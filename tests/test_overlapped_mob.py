"""
test_overlapped_mob.py: Project 6 - Tester with Python

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

@pytest.mark.slow
@pytest.mark.parametrize(
        ('menu_sel', 'last_item_sel', 'overlay_sel'),
        [
            (
                '#main-header label.mobile-menu-toggle',
                '#top-menu > li',
                '#main-header > div > div > nav > div.menu-buttons-mobile-default'
            ),
            (
                '#open-courses-menu',
                '#courses-dropdown > li:nth-child(3) > ul > li',
                '#main-header > div > div > nav > div.menu-buttons-mobile-courses'
            )
        ]
        )
def test_visibility(page: Page, menu_sel: str, last_item_sel: str, overlay_sel: str):
    """
    Verifies that the last menu item is visible and not overlapped by overlays
    after toggling mobile menus.

    Args:
        page (Page): The Playwright page object.
        menu_sel (str): Selector for the main menu toggle button.
        last_item_sel (str): Selector for the last menu item.
        overlay_sel (str): Selector for the relevant overlay element.

    Asserts:
        - The last menu item is visible and has a bounding box.
        - No overlay obstructs the last menu item.
    """
    page.goto(URL)
    refuse_cookies(page)
    menu_toggle = page.locator(menu_sel)
    menu_toggle.click()

    sub_menu_guide = page.locator('#top-menu > li.area-pruvodce > label')
    if sub_menu_guide.is_visible():
        sub_menu_guide.click()

    sub_menu_about = page.locator('#top-menu > li.area-onas > label')
    if sub_menu_about.is_visible():
        sub_menu_about.click()

    last_item = page.locator(last_item_sel).last
    assert last_item.is_visible(), 'Last item is not visible.'

    last_item_box = last_item.bounding_box()
    assert last_item_box is not None, 'Last item bounding box not found.'

    overlays = [
        page.locator(overlay_sel),
        page.locator('#cookiescript_badge'),
        page.locator('#cookiescript_reject'),
        page.locator('div.intercom-lightweight-app > div')
    ]
    for overlay in overlays:
        if overlay.is_visible():
            overlay_box = overlay.bounding_box()
            assert overlay_box is not None, 'Overlay bounding box not found.'

            def boxes_intersect(box1, box2):
                return not (
                        box1['x'] + box1['width'] < box2['x'] or
                        box2['x'] + box2['width'] < box1['x'] or
                        box1['y'] + box1['height'] < box2['y'] or
                        box2['y'] + box2['height'] < box1['y']
                    )
            assert not boxes_intersect(last_item_box, overlay_box), 'Last item is covered.'
