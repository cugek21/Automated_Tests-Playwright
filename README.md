# Automated Tests - Playwright

This project contains automated tests for web applications using Python and Playwright. The tests are organized to check for broken links, indentation issues, overlapped elements, and response times, primarily targeting mobile scenarios.

## Project Structure

- `tests/` - All test scripts and utilities:
  - `test_broken_links.py`: Detects broken links by fetching all links from the main page and checking their HTTP status codes.
  - `test_indentation_mob.py`: Ensures header elements are visible and properly indented on mobile layouts.
  - `test_overlapped_mob.py`: Verifies that the last menu item in mobile navigation is visible and not overlapped by overlays (e.g., cookie banners, chat widgets).
  - `test_response_time.py`: Checks that all fetched links respond within the configured `TIMEOUT` (see `conftest.py`).
  - `utils.py`: Utility functions for extracting and normalizing hyperlinks from web pages.
  - `conftest.py`: Shared fixtures for browser setup, viewport, context, and cookie handling. Defines shared configuration variables such as `URL`, `BLOCKED_DOMAINS`, `VIEWPORTS`, and `TIMEOUT` (used for response time tests).
  - `__init__.py`: Marks the directory as a Python package.
- `pytest.ini` - Pytest configuration and custom markers.
- `requirements.txt` - Python dependencies for the project.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Install Playwright browsers:**
   ```bash
   playwright install
   ```
3. **Run tests:**
   ```bash
   pytest
   ```

## Test Descriptions

- **Broken Links:**
  - Scans the main page for all links (excluding blocked domains) and asserts that each returns a valid HTTP status code (<400).
- **Indentation (Mobile):**
  - Checks that key header elements are visible and indented by at least 16px from the left edge on mobile viewports.
- **Overlapped Menu (Mobile):**
  - Ensures the last menu item is visible and not covered by overlays after toggling mobile menus.
- **Response Time:**
  - Asserts that all fetched links respond in under the configured `TIMEOUT` (see `conftest.py`).
## Configuration

- The `TIMEOUT` variable (used for response time tests) and other shared settings are defined in `tests/conftest.py` for easy centralized management.

## Utilities & Fixtures

- **utils.py:**
  - `fetch_links(url, blocked_domains)`: Extracts and normalizes all valid hyperlinks from a page, filtering out blocked domains and unsupported schemes. Logs skipped and blocked links.
- **conftest.py:**
  - Provides fixtures for browser type, viewport, context options, Playwright page, and cookie refusal. Logs browser actions and cookie handling.

## Logging

All tests and utilities use Python's built-in `logging` module for runtime diagnostics. Log messages include information about browser actions, skipped/blocked links, test steps, and errors.

- By default, log level is set to `INFO`.
- To change the log level, edit the `logging.basicConfig(level=logging.INFO, ...)` line in your test files or `conftest.py`.
- Log output appears in the console during test runs.

## Troubleshooting

- Review log output for details on test execution, skipped links, browser actions, and errors.
- If a test fails, check the log for the relevant error or warning message.


## Requirements
- Python 3.10+
- Playwright
- Pytest

## Notes
- Tests are designed for both mobile and desktop web scenarios.
- You can deselect slow tests with:
  ```bash
  pytest -m "not slow"
  ```
- The `HEADLESS` environment variable can be set to `false` to run browsers in headed mode.

## Author
Radek Jíša
