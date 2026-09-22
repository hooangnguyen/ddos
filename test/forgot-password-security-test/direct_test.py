from browser_session import create_session
from token_provider import (
    extract_csrf,
    extract_iframe_token
)

from vinfast_client import (
    VinFastForgotPassword
)


LOGIN_PAGE = (
    "https://shop.vinfastauto.com/"
    "vn_vi/login/iframe"
)


# thay bằng email test của bạn
TEST_EMAIL = "test@gmail.com"



print("[1] Create session")

session = create_session()



print("[2] Get login iframe")

response = session.get(
    LOGIN_PAGE,
    timeout=15
)


html = response.text



print("[3] Extract tokens")


csrf_token = extract_csrf(
    html
)


iframe_token = extract_iframe_token(
    html
)



print(
    "CSRF found:",
    bool(csrf_token)
)


print(
    "Iframe token found:",
    bool(iframe_token)
)



if not csrf_token or not iframe_token:

    print(
        "[-] Cannot extract token"
    )

    exit()



print("[4] Send forgot password request")



client = VinFastForgotPassword(
    session=session
)


result = client.forgot_password(

    TEST_EMAIL,

    csrf_token,

    iframe_token

)



print("[5] Response")

print(result)
