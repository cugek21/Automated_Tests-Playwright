"""
test_response_time.py: Project 6 - Tester with Python

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
def test_response_time(link: str):
    """
    Test that the given link responds quickly without errors.

    Args:
        link (str): The URL to test.

    Asserts:
        - The HTTP request completes without exceptions.
        - The response time is less than 0.5 seconds (500 ms).

    Raises:
        AssertionError: If the response time exceeds 0.5 seconds or
                        if a request exception occurs.
    """
    timeout = 0.5 # in seconds
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }
    try:
        response = requests.get(link, headers=headers, timeout=10)
        assert response.elapsed.total_seconds() < timeout, \
            f'Slow link: {link}, Response Time: {response.elapsed.total_seconds()*1000} ms'
    except requests.RequestException as e:
        assert False, f'Request: {link}, Error: {e}'
