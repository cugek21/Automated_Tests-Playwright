"""
utils.py

Utility functions for Playwright-based automated tests.
Includes functions for extracting and normalizing hyperlinks from web pages.

Author: Radek Jíša
Email: radek.jisa@gmail.com
"""

import logging
import os
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright

logger = logging.getLogger(__name__)

def fetch_links(url: str, blocked_domains) -> list[str]:
    """
    Extracts and normalizes all valid hyperlinks from the given webpage.

    Args:
        url (str): The URL of the webpage to scan.
        blocked_domains (list[str]): List of domain substrings to exclude from results.

    Returns:
        list[str]: A list of absolute URLs found on the page,
        excluding blocked and unsupported links.
    """
    headless_env = os.getenv("HEADLESS", "true").lower()
    headless = headless_env == "true"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        locator = page.locator('a[href]')
        links = set()
        count = locator.count()

        for i in range(count):
            href = locator.nth(i).get_attribute('href')
            if not href:
                logger.info("Skipped: Empty -> index %s", i)
                continue
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                logger.info("Skipped: Unsupported -> %s", href)
                continue
            full_url = urljoin(url, href)
            if any(domain in full_url for domain in blocked_domains):
                logger.info("Skipped: Blocked -> %s", full_url)
                continue
            links.add(full_url)
        browser.close()
    logger.info("Total valid links: %d from %d", len(links), count)
    return list(links)
