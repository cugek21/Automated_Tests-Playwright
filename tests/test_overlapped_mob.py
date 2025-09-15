"""
Automated test for verifying that the last menu item in a mobile menu is visible
and not overlapped by overlays.

The test toggles mobile menus, interacts with submenus,
and checks for visual obstructions from overlays such as cookie banners or chat widgets.

Author: Radek Jíša
Email: radek.jisa@gmail.com
"""


import logging

import pytest
from playwright.sync_api import Page

from tests.conftest import URL


logger = logging.getLogger(__name__)


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
def test_visibility(page: Page, refuse_cookies, menu_sel: str, last_item_sel: str, overlay_sel: str):
    """
    Verifies that the last menu item is visible and not overlapped by overlays
    after toggling mobile menus.

    Args:
        page (Page): The Playwright page object.
        refuse_cookies: Fixture to refuse cookies (callable).
        menu_sel (str): Selector for the main menu toggle button.
        last_item_sel (str): Selector for the last menu item.
        overlay_sel (str): Selector for the relevant overlay element.

    Raises:
        AssertionError: If the last menu item is not visible,
        has no bounding box, or is covered by an overlay.
    """
    page.goto(URL)
    refuse_cookies()

    menu_toggle = page.locator(menu_sel)
    if menu_toggle.is_visible():
        logger.info('Clicking menu toggle: %s', menu_sel)
        menu_toggle.click()

    sub_menu_guide = page.locator('#top-menu > li.area-pruvodce > label')
    if sub_menu_guide.is_visible():
        logger.debug('Clicking submenu: #top-menu > li.area-pruvodce > label')
        sub_menu_guide.click()

    sub_menu_about = page.locator('#top-menu > li.area-onas > label')
    if sub_menu_about.is_visible():
        logger.debug('Clicking submenu: #top-menu > li.area-onas > label')
        sub_menu_about.click()

    last_item = page.locator(last_item_sel).last
    if not last_item.is_visible():
        logger.warning('Last item is not visible: %s', last_item)
    assert last_item.is_visible(), 'Last item is not visible.'

    last_item_box = last_item.bounding_box()
    logger.debug("Last item bounding box: %s", last_item_box)
    if last_item_box is None:
        logger.warning('Last item bounding box not found: %s', last_item_box)
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
            if overlay_box is None:
                logger.warning("Overlay bounding box not found: %s", overlay_box)
            assert overlay_box is not None, 'Overlay bounding box not found.'
            logger.info("Checking overlay bounding box: %s", overlay_box)

            def boxes_intersect(box1, box2):
                return not (
                    box1['x'] + box1['width'] < box2['x'] or
                    box2['x'] + box2['width'] < box1['x'] or
                    box1['y'] + box1['height'] < box2['y'] or
                    box2['y'] + box2['height'] < box1['y']
                )
            if boxes_intersect(last_item_box, overlay_box):
                logger.error("Last item is covered by overlay: %s", overlay_box)
            assert not boxes_intersect(last_item_box, overlay_box), 'Last item is covered.'
