"""
test_broken_links.py: Project 6 - Tester with Python

author: Radek Jíša
email: radek.jisa@gmail.com
"""

from urllib.parse import urljoin

import pytest
import requests
from playwright.sync_api import sync_playwright

URL = 'https://engeto.cz/'
BLOCKED_DOMAINS = [
            'facebook.com', 
            'youtube.com', 
            'instagram.com', 
            'linkedin.com', 
            'discord.gg'
            ]

def fetch_links(url: str) -> list[str]:
    """
    Extracts and normalizes all valid hyperlinks from the given webpage.

    Args:
        url (str): The URL of the webpage to scan.

    Returns:
        list[str]: A list of absolute URLs found on the page.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto(url)

        locator = page.locator('a[href]')
        links = set()
        count = locator.count()

        for i in range(count):
            href = locator.nth(i).get_attribute('href')
            if not href:
                print(f'\nSkipped: Empty -> index {i}')
                continue
            if href.startswith(('mailto:', 'tel:', 'javascript:', '#')):
                print(f'Skipped: Unsupported -> {href}')
                continue
            full_url = urljoin(url, href)
            if any(domain in full_url for domain in BLOCKED_DOMAINS):
                print(f'Skipped: Blocked -> {full_url}')
                continue
            links.add(full_url)
        browser.close()
        print(f'\nTotal valid links: {len(links)} from {count}\n')
        return list(links)

LINKS = fetch_links(URL)

@pytest.mark.parametrize(('link'), LINKS)
def test_broken_links(link: str):
    """
    Checks if a given link returns a valid (non-error) HTTP status code.

    Args:
        link (str): A full URL to test.

    Asserts:
        The HTTP status code must be less than 400,
        otherwise the test fails with the link and error info.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }
    try:
        response = requests.get(link, headers=headers, timeout=10)
        assert response.status_code < 400, \
            f'Broken link: {link}, Status: {response.status_code}'
    except requests.RequestException as e:
        assert False, f'Request: {link}, Error: {e}'
