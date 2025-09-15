"""
test_broken_links.py

Automated test for detecting broken links on a web page.
Fetches all links from the target URL, filters out blocked domains,
and checks each link for a valid HTTP response.

Author: Radek Jíša
Email: radek.jisa@gmail.com
"""

import logging

import pytest
import requests

from tests.utils import fetch_links
from tests.conftest import URL, BLOCKED_DOMAINS

logger = logging.getLogger(__name__)

LINKS = fetch_links(URL, BLOCKED_DOMAINS)

@pytest.mark.parametrize(('link'), LINKS)
def test_broken_links(link: str):
    """
    Checks if a given link returns a valid (non-error) HTTP status code.

    Args:
        link (str): The URL to be tested.

    Raises:
        AssertionError: If the link is broken or the request fails.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }
    logger.info('Checking link: %s', link)
    try:
        response = requests.get(link, headers=headers, timeout=10)
        if response.status_code >= 400:
            logger.error('Broken link: %s, Status: %s', link, response.status_code)
        assert response.status_code < 400, \
            f'Broken link: {link}, Status: {response.status_code}'
    except requests.RequestException as e:
        logger.error('Request failed for link: %s, Error: %s', link, e)
        assert False, f'Request: {link}, Error: {e}'
