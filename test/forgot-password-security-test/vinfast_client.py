import requests

from config import (
    VINFAST_ENDPOINT,
    HEADERS,
    RECAPTCHA_TOKEN
)


class VinFastForgotPassword:

    def __init__(self, session=None):

        if session:
            self.session = session
        else:
            self.session = requests.Session()

        self.session.headers.update(
            HEADERS
        )


    def forgot_password(
        self,
        email,
        csrf_token,
        iframe_token
    ):

        data = {

            "loginEmail": email,

            "grecaptcha_token1": "",

            "grecaptcha_token": RECAPTCHA_TOKEN,

            "csrf_token": csrf_token,

            "iframeLoginToken": iframe_token

        }


        headers = HEADERS.copy()



        print("\n===== DEBUG REQUEST =====")

        print("\nURL:")
        print(VINFAST_ENDPOINT)


        print("\nHEADERS:")
        print(headers)


        print("\nDATA:")

        debug_data = data.copy()

        if "grecaptcha_token" in debug_data:
            debug_data["grecaptcha_token"] = "***HIDDEN***"

        if "csrf_token" in debug_data:
            debug_data["csrf_token"] = "***HIDDEN***"

        if "iframeLoginToken" in debug_data:
            debug_data["iframeLoginToken"] = "***HIDDEN***"


        print(debug_data)


        print("\nCOOKIES:")
        print(
            self.session.cookies.get_dict()
        )


        print("========================")



        try:

            response = self.session.post(

                VINFAST_ENDPOINT,

                data=data,

                headers=headers,

                timeout=15

            )


        except Exception as e:

            print("[!] Request error:")
            print(e)

            return {

                "email": email,

                "error": str(e)

            }



        print("\n===== DEBUG RESPONSE =====")


        print("\nSTATUS:")
        print(response.status_code)


        print("\nHEADERS:")
        print(dict(response.headers))


        print("\nBODY:")

        print(
            response.text[:2000]
        )


        print("==========================\n")



        try:

            result = response.json()


        except Exception:

            result = {

                "raw": response.text

            }



        return {

            "email": email,

            "status_code": response.status_code,

            "response": result

        }