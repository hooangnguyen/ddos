import requests


LOGIN_PAGE = (
    "https://shop.vinfastauto.com/"
    "vn_vi/login/iframe"
)



def create_session():

    session = requests.Session()


    session.headers.update({

        "User-Agent":
        (
            "Mozilla/5.0 "
            "(X11; Linux x86_64) "
            "AppleWebKit/537.36 "
            "Chrome/153 Safari/537.36"
        )

    })


    response = session.get(
        LOGIN_PAGE,
        timeout=15
    )


    print(
        "[+] Login page status:",
        response.status_code
    )


    return session