from browser_session import create_session
from token_provider import (
    extract_csrf,
    extract_iframe_token
)


session = create_session()


response = session.get(
    "https://shop.vinfastauto.com/vn_vi/login/iframe"
)


html = response.text


csrf = extract_csrf(html)

iframe = extract_iframe_token(html)


print(
    "CSRF:",
    csrf
)


print(
    "IFRAME:",
    iframe
)