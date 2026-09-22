# main.py

from browser_session import (
    create_session
)

from token_provider import (
    extract_csrf,
    extract_iframe_token
)

from vinfast_client import (
    VinFastForgotPassword
)

from random_email import (
    generate_emails
)

from report import (
    save_report
)


LOGIN_PAGE = (
    "https://shop.vinfastauto.com/"
    "vn_vi/login/iframe"
)


# số lượng email random muốn test
TEST_COUNT = 10



def main():

    print(
        "[+] Create session"
    )


    session = create_session()



    print(
        "[+] Load login iframe"
    )


    response = session.get(
        LOGIN_PAGE,
        timeout=15
    )


    html = response.text



    print(
        "[+] Extract token"
    )


    csrf_token = extract_csrf(
        html
    )


    iframe_token = extract_iframe_token(
        html
    )



    if not csrf_token:

        print(
            "[-] csrf_token not found"
        )

        return



    if not iframe_token:

        print(
            "[-] iframeLoginToken not found"
        )

        return



    print(
        "[+] Token OK"
    )



    client = VinFastForgotPassword(
        session=session
    )



    emails = generate_emails(
        TEST_COUNT
    )


    results = []



    for index, email in enumerate(
        emails,
        start=1
    ):


        print(
            f"[{index}/{TEST_COUNT}] Testing: {email}"
        )


        result = client.forgot_password(

            email,

            csrf_token,

            iframe_token

        )


        results.append(
            result
        )



    report = {

        "test_count":
            TEST_COUNT,


        "results":
            results

    }



    save_report(
        report
    )


    print(
        "[+] Finished"
    )



if __name__ == "__main__":

    main()