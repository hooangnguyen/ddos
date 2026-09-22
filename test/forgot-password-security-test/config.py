"""
Configuration
"""

# config.py


VINFAST_ENDPOINT = (
    "https://shop.vinfastauto.com/"
    "on/demandware.store/"
    "Sites-app_vinfast_vn-Site/"
    "vi_VN/Login-Auth0ForgotPassword"
)



HEADERS = {

    "Accept":
        "application/json, text/javascript, */*; q=0.01",

    "Content-Type":
        "application/x-www-form-urlencoded; charset=UTF-8",

    "Origin":
        "https://shop.vinfastauto.com",

    "Referer":
        "https://shop.vinfastauto.com/vn_vi/login/iframe",

    "X-Requested-With":
        "XMLHttpRequest",

    "User-Agent":
        (
            "Mozilla/5.0 "
            "(X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "Chrome/153 Safari/537.36"
        )
}



# Token captcha lấy từ phiên test hợp lệ
RECAPTCHA_TOKEN = ""
