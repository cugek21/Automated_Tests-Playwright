# Automated Tests - Playwright

This project contains automated tests for web applications using Python and Playwright. The tests are organized to check for broken links, indentation issues, overlapped elements, and response times, primarily targeting mobile scenarios.

## Project Structure

- `tests/` - Contains all test scripts:
  - `test_broken_links.py`: Checks for broken links on web pages.
  - `test_indentation_mob.py`: Verifies indentation issues on mobile views.
  - `test_overlapped_mob.py`: Detects overlapped elements in mobile layouts.
  - `test_response_time.py`: Measures response times for web requests.
- `pytest.ini` - Configuration for pytest.
- `requirements.txt` - Python dependencies for the project.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run tests:**
   ```bash
   pytest
   ```

## Requirements
- Python 3.10+
- Playwright
- Pytest

## Notes
- Make sure to install Playwright browsers if not already done:
  ```bash
  playwright install
  ```
- Tests are designed for mobile and desktop web scenarios.

## License
MIT License
