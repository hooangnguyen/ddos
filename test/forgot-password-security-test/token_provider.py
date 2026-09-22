
import re
from html import unescape


def _find_input_value(html: str, field_name: str):
    """
    Find a hidden/input field by name and return its value.

    Does not print or expose the token.
    """

    patterns = [
        # name="field" ... value="..."
        rf'<input\b[^>]*\bname=["\']{re.escape(field_name)}["\'][^>]*\bvalue=["\']([^"\']*)["\']',

        # value="..." ... name="field"
        rf'<input\b[^>]*\bvalue=["\']([^"\']*)["\'][^>]*\bname=["\']{re.escape(field_name)}["\']',
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:
            value = unescape(match.group(1)).strip()

            if value:
                return value

    return None


def _find_js_value(html: str, field_name: str):
    """
    Fallback for simple JavaScript/object assignments.

    This is only a parser fallback; it does not generate tokens.
    """

    pattern = (
        rf'["\']?{re.escape(field_name)}["\']?'
        rf'\s*[:=]\s*["\']([^"\']+)["\']'
    )

    match = re.search(
        pattern,
        html,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if match:
        return unescape(match.group(1)).strip()

    return None


def _find_meta_value(html: str, field_name: str):
    """
    Find a meta tag by name and return its content value.
    """
    patterns = [
        # name="field" ... content="..."
        rf'<meta\b[^>]*\bname=["\']{re.escape(field_name)}["\'][^>]*\bcontent=["\']([^"\']*)["\']',
        # content="..." ... name="field"
        rf'<meta\b[^>]*\bcontent=["\']([^"\']*)["\'][^>]*\bname=["\']{re.escape(field_name)}["\']',
    ]

    for pattern in patterns:
        match = re.search(
            pattern,
            html,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if match:
            value = unescape(match.group(1)).strip()

            if value:
                return value

    return None


def extract_value(html: str, field_name: str):
    value = _find_meta_value(
        html,
        field_name,
    )

    if value:
        return value

    value = _find_input_value(
        html,
        field_name,
    )

    if value:
        return value

    return _find_js_value(
        html,
        field_name,
    )


def extract_csrf(html: str):
    return extract_value(
        html,
        "csrf_token",
    )


def extract_iframe_token(html: str):
    return extract_value(
        html,
        "iframeLoginToken",
    )


def token_debug_info(token):
    """
    Safe diagnostic information.
    Never returns the token itself.
    """

    if not token:
        return {
            "present": False,
            "length": 0,
        }

    return {
        "present": True,
        "length": len(token),
    }

