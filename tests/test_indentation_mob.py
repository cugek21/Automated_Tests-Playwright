"""
Automated test for verifying that header elements on the mobile page
are visible and properly indented from the left edge. Checks multiple
header selectors for visibility and minimum indentation.
"""

import logging

import pytest
from playwright.sync_api import Page

from tests.conftest import URL

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
        ('header_sel'),
        [
            ("#logo"),
            ("main h1:has-text('Staň se novým IT talentem')"),
            ("main a:has-text('Přehled IT kurzů')"),
            ("main h2:has-text('Přečti si o IT, kariéře a trhu práce')")
        ]
        )
def test_indentation(page: Page, refuse_cookies, header_sel: str):
    """
    Verifies that a given header element is visible and properly
    indented from the left edge of the page.

    Args:
        page (Page): The Playwright page object.
        refuse_cookies: Fixture to refuse cookies (callable).
        header_sel (str): CSS selector for the header element.

    Raises:
        AssertionError: If the header is not visible, has no bounding
        box, or is not indented by at least 16 pixels.
    """
    page.goto(URL)
    refuse_cookies()

    logger.info('Checking header: %s', header_sel)
    header = page.locator(header_sel)
    if not header.is_visible():
        logger.warning('Header is not visible: %s', header_sel)
    assert header.is_visible(), 'Header is not visible.'

    header_box = header.bounding_box()
    if header_box is None:
        logger.warning('Header bounding box not found: %s', header_sel)
    assert header_box is not None, 'Header bounding box not found.'

    if header_box['x'] < 16:
        logger.error(
            "Header '%s' x position: %s", header_sel, header_box['x']
        )
    else:
        logger.info(
            "Header '%s' x position: %s", header_sel, header_box['x']
        )
    assert header_box['x'] >= 16, 'Header is not indented.'
