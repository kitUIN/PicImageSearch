#!/usr/bin/env python3
"""Fetch Copyseeker Next.js server action tokens and update constants.py."""

import re
import sys
from json import dumps as json_dumps
from pathlib import Path
from typing import NoReturn

import httpx

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONSTANTS_FILE = PROJECT_ROOT / "PicImageSearch" / "constants.py"

COPYSEEKER_URL = "https://copyseeker.net"
COPYSEEKER_DISCOVERY_URL = f"{COPYSEEKER_URL}/discovery"
HTTP_TIMEOUT_SECONDS = 20.0

DISCOVERY_ACTION_NAMES = ("triggerDiscovery", "triggerDiscoveryByFile", "SetCookie")
RESULTS_ACTION_NAME = "getReverseImageSearchDiscovery"

JS_CHUNK_PATTERN = re.compile(r"(?:/_next/)?static/chunks/[^\"'<>\s]+?\.js")
COPYSEEKER_CONSTANTS_PATTERN = re.compile(r"COPYSEEKER_CONSTANTS\s*=\s*\{.*?\}", re.DOTALL)


def fail(message: str) -> NoReturn:
    """Print an error message and stop the script."""
    print(f"Error: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_constants_file_exists() -> None:
    """Ensure the target constants file exists before making network requests."""
    if not CONSTANTS_FILE.exists():
        fail(f"constants.py file does not exist: {CONSTANTS_FILE}")


def get_js_chunk_urls(html: str) -> list[str]:
    """Extract unique Next.js chunk URLs from a page."""
    js_urls: list[str] = []
    seen: set[str] = set()

    for chunk_path in JS_CHUNK_PATTERN.findall(html):
        # Copyseeker may reference chunks with or without the /_next prefix.
        normalized_path = chunk_path if chunk_path.startswith("/_next/") else f"/_next/{chunk_path}"
        full_url = f"{COPYSEEKER_URL}{normalized_path}"

        if full_url not in seen:
            seen.add(full_url)
            js_urls.append(full_url)

    return js_urls


def extract_next_action_token(js_content: str, action_name: str) -> str | None:
    """Extract a Next.js server action token for a named action from JavaScript."""
    token_pattern = rf'\("([a-f0-9]+)"[^"]+"{re.escape(action_name)}"'
    if match := re.search(token_pattern, js_content):
        return match[1]
    return None


def fetch_next_action_tokens(page_url: str, action_names: tuple[str, ...]) -> dict[str, str | None]:
    """Get Next.js server action tokens from all chunks referenced by a page."""
    tokens: dict[str, str | None] = {action_name: None for action_name in action_names}

    with httpx.Client(timeout=HTTP_TIMEOUT_SECONDS) as client:
        response = client.get(page_url).raise_for_status()

        for js_url in get_js_chunk_urls(response.text):
            js_response = client.get(js_url).raise_for_status()
            js_content = js_response.text

            for action_name in action_names:
                if tokens[action_name] is not None or action_name not in js_content:
                    continue

                tokens[action_name] = extract_next_action_token(js_content, action_name)

            if all(token is not None for token in tokens.values()):
                break

    return tokens


def fetch_discovery_action_tokens() -> tuple[str | None, str | None, str | None]:
    """Get next-action tokens for URL search, file upload, and SetCookie."""
    try:
        tokens = fetch_next_action_tokens(COPYSEEKER_URL, DISCOVERY_ACTION_NAMES)
        return (
            tokens["triggerDiscovery"],
            tokens["triggerDiscoveryByFile"],
            tokens["SetCookie"],
        )
    except httpx.HTTPError as exc:
        print(f"Failed to get next-action tokens for discovery actions: {exc}", file=sys.stderr)
        return None, None, None


def fetch_results_action_token() -> str | None:
    """Get next-action token for search results."""
    try:
        tokens = fetch_next_action_tokens(COPYSEEKER_DISCOVERY_URL, (RESULTS_ACTION_NAME,))
        return tokens[RESULTS_ACTION_NAME]
    except httpx.HTTPError as exc:
        print(f"Failed to get next-action token for search results: {exc}", file=sys.stderr)
        return None


def update_constants_file(url_token: str, file_token: str, set_cookie_token: str, results_token: str) -> None:
    """Update tokens in constants.py."""
    content = CONSTANTS_FILE.read_text(encoding="utf-8")

    new_constants = {
        "URL_SEARCH_TOKEN": url_token,
        "FILE_UPLOAD_TOKEN": file_token,
        "SET_COOKIE_TOKEN": set_cookie_token,
        "GET_RESULTS_TOKEN": results_token,
    }

    constants_str = f"COPYSEEKER_CONSTANTS = {json_dumps(new_constants, indent=4)}"
    new_content, replacement_count = COPYSEEKER_CONSTANTS_PATTERN.subn(constants_str, content, count=1)

    if replacement_count != 1:
        fail(f"unable to find COPYSEEKER_CONSTANTS in {CONSTANTS_FILE}")

    _ = CONSTANTS_FILE.write_text(new_content, encoding="utf-8")


def handle_missing_tokens(
    url_token: str | None, file_token: str | None, set_cookie_token: str | None, results_token: str | None
) -> NoReturn:
    """Report missing tokens and stop the script."""
    token_labels = {
        "URL search token": url_token,
        "file upload token": file_token,
        "set cookie token": set_cookie_token,
        "get results token": results_token,
    }
    missing = [label for label, token in token_labels.items() if not token]

    fail(f"update failed. Unable to get the following tokens: {', '.join(missing)}")


def update_copyseeker_tokens(url_token: str, file_token: str, set_cookie_token: str, results_token: str) -> None:
    """Display retrieved tokens and update constants.py."""
    print(f"URL search token: {url_token}")
    print(f"File upload token: {file_token}")
    print(f"Set cookie token: {set_cookie_token}")
    print(f"Get results token: {results_token}")

    update_constants_file(url_token, file_token, set_cookie_token, results_token)
    print("Successfully updated constants.py file!")


def main() -> None:
    ensure_constants_file_exists()
    print("Starting to update Copyseeker next-action tokens...")

    url_token, file_token, set_cookie_token = fetch_discovery_action_tokens()
    results_token = fetch_results_action_token()

    if not (url_token and file_token and set_cookie_token and results_token):
        handle_missing_tokens(url_token, file_token, set_cookie_token, results_token)

    update_copyseeker_tokens(url_token, file_token, set_cookie_token, results_token)


if __name__ == "__main__":
    main()
