#!/usr/bin/env python3
"""
Copyseeker Tokens Update Script

This script retrieves the latest next-action tokens and set-cookie token from the Copyseeker website,
and updates the corresponding values in the PicImageSearch/constants.py file.

Usage:
1. Install dependencies: pip install httpx
2. Run script: python .github/scripts/update_copyseeker_tokens.py
"""

import re
import sys
from json import dumps as json_dumps
from pathlib import Path
from typing import Optional

import httpx

# Get project root directory
project_root = Path(__file__).resolve().parents[2]

constants_file = project_root / "PicImageSearch" / "constants.py"

# Confirm constants.py file exists
if not constants_file.exists():
    print(f"Error: constants.py file does not exist: {constants_file}")
    sys.exit(1)

# Website URLs
COPYSEEKER_URL = "https://copyseeker.net"
COPYSEEKER_DISCOVERY_URL = f"{COPYSEEKER_URL}/discovery"


def fetch_url_search_and_file_upload_token():
    """Get next-action token for URL search and file upload"""
    try:
        with httpx.Client() as client:
            response = client.get(COPYSEEKER_URL)
            response.raise_for_status()  # pyright: ignore[reportUnusedCallResult]

            # Find links containing JS files
            js_urls = re.findall(r'static/chunks/[^"]+\.js', response.text)

            # Find JS files containing triggerDiscovery
            for js_url in js_urls:
                full_url = f"{COPYSEEKER_URL}/_next/{js_url}"
                js_content = client.get(full_url).text

                # Check if it contains the target function
                if "triggerDiscovery" not in js_content:
                    continue

                url_match = re.search(r'\("([a-f0-9]+)"[^"]+"triggerDiscovery"', js_content)
                file_match = re.search(r'\("([a-f0-9]+)"[^"]+"triggerDiscoveryByFile"', js_content)
                set_cookie_match = re.search(r'\("([a-f0-9]+)"[^"]+"SetCookie"', js_content)

                url_token = url_match[1] if url_match else None
                file_token = file_match[1] if file_match else None
                set_cookie_token = set_cookie_match[1] if set_cookie_match else None

                if url_token and file_token and set_cookie_token:
                    return url_token, file_token, set_cookie_token

            return None, None, None
    except Exception as e:
        print(f"Failed to get next-action token for URL search and file upload: {e}")
        return None, None, None


def fetch_get_results_token():
    """Get next-action token for search results"""
    try:
        with httpx.Client() as client:
            response = client.get(COPYSEEKER_DISCOVERY_URL)
            response.raise_for_status()  # pyright: ignore[reportUnusedCallResult]

            # Find target JS files
            js_urls = re.findall(r'static/chunks/app/discovery/page-[^"]+\.js', response.text)

            # Find JS files containing target function
            for js_url in js_urls:
                full_url = f"{COPYSEEKER_URL}/_next/{js_url}"
                js_content = client.get(full_url).text

                # Check and extract token
                if "getReverseImageSearchDiscovery" in js_content:
                    if match := re.search(r'\("([a-f0-9]+)"[^"]+"getReverseImageSearchDiscovery"', js_content):
                        return match[1]

            return None
    except Exception as e:
        print(f"Failed to get next-action token for search results: {e}")
        return None


def update_constants_file(url_token: str, file_token: str, set_cookie_token: str, results_token: str):
    """Update tokens in the constants.py file"""
    # Read current file content
    content = constants_file.read_text(encoding="utf-8")

    # Create new COPYSEEKER_CONSTANTS dictionary
    new_constants = {
        "URL_SEARCH_TOKEN": url_token,
        "FILE_UPLOAD_TOKEN": file_token,
        "SET_COOKIE_TOKEN": set_cookie_token,
        "GET_RESULTS_TOKEN": results_token,
    }

    # Find and replace COPYSEEKER_CONSTANTS dictionary
    constants_pattern = r"COPYSEEKER_CONSTANTS\s*=\s*\{[^}]+\}"
    constants_str = f"COPYSEEKER_CONSTANTS = {json_dumps(new_constants, indent=4)}"

    # Replace old constants content
    new_content = re.sub(constants_pattern, constants_str, content)

    # Write to file
    constants_file.write_text(new_content, encoding="utf-8")  # pyright: ignore[reportUnusedCallResult]


def handle_missing_tokens(
    url_token: Optional[str], file_token: Optional[str], set_cookie_token: Optional[str], results_token: Optional[str]
):
    """Handle missing tokens and output error messages"""
    missing = []
    if not url_token:
        missing.append("URL search token")
    if not file_token:
        missing.append("file upload token")
    if not set_cookie_token:
        missing.append("set cookie token")
    if not results_token:
        missing.append("get results token")

    print(f"Update failed. Unable to get the following tokens: {', '.join(missing)}")
    sys.exit(1)


def main():
    print("Starting to update Copyseeker next-action tokens...")

    # Get tokens
    url_token, file_token, set_cookie_token = fetch_url_search_and_file_upload_token()
    results_token = fetch_get_results_token()

    # Check if all tokens were retrieved
    if url_token and file_token and set_cookie_token and results_token:
        update_copyseeker_tokens(url_token, file_token, set_cookie_token, results_token)
    else:
        handle_missing_tokens(url_token, file_token, set_cookie_token, results_token)


def update_copyseeker_tokens(url_token: str, file_token: str, set_cookie_token: str, results_token: str):
    # Display retrieved tokens
    print(f"URL search token: {url_token}")
    print(f"File upload token: {file_token}")
    print(f"Set cookie token: {set_cookie_token}")
    print(f"Get results token: {results_token}")

    # Update constants.py file
    update_constants_file(url_token, file_token, set_cookie_token, results_token)
    print("Successfully updated constants.py file!")


if __name__ == "__main__":
    main()
