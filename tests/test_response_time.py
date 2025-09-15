"""
test_response_time.py

Automated test for verifying that all fetched links from the main URL
respond within an acceptable time limit.
Checks that each link responds in less than the configured TIMEOUT (see conftest.py) and
does not raise request exceptions.

The TIMEOUT value is defined in conftest.py and imported for consistency across tests.

Author: Radek Jíša
Email: radek.jisa@gmail.com
"""

import logging

import pytest
import requests

from tests.utils import fetch_links
from tests.conftest import URL, BLOCKED_DOMAINS, TIMEOUT

logger = logging.getLogger(__name__)

LINKS = fetch_links(URL, BLOCKED_DOMAINS)

@pytest.mark.slow
@pytest.mark.parametrize(('link'), LINKS)
def test_response_time(link: str):
    """
    Test that the given link responds quickly without errors.

    Args:
        link (str): The URL to be tested.

    Raises:
        AssertionError: If the response time exceeds 0.5 seconds or
        if a request exception occurs.
    """
    timeout = TIMEOUT
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/115.0.0.0 Safari/537.36'
        )
    }
    logger.info('Checking response time for link: %s', link)
    try:
        response = requests.get(link, headers=headers, timeout=10)
        elapsed = response.elapsed.total_seconds()
        if elapsed >= timeout:
            logger.warning('Slow link: %s, Response Time: %.2f ms', link, elapsed*1000)
        assert elapsed < timeout, \
            f'Slow link: {link}, Response Time: {elapsed*1000} ms'
    except requests.RequestException as e:
        logger.error('Request failed for link: %s, Error: %s', link, e)
        assert False, f'Request: {link}, Error: {e}'
