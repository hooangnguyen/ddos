
from browser_session import create_session
from token_provider import (
    extract_csrf,
    extract_iframe_token,
    token_debug_info,
)


LOGIN_PAGE = (
    "https://shop.vinfastauto.com/"
    "vn_vi/login/iframe"
)


session = create_session()

response = session.get(
    LOGIN_PAGE,
    timeout=15,
)

print("HTTP status:", response.status_code)
print("Final URL:", response.url)

html = response.text

csrf = extract_csrf(html)
iframe = extract_iframe_token(html)

print("CSRF:", token_debug_info(csrf))
print("iframeLoginToken:", token_debug_info(iframe))

print("\nCookies:")
for cookie in session.cookies:
    print(
        f"- {cookie.name}: "
        f"domain={cookie.domain}, "
        f"path={cookie.path}"
    )

