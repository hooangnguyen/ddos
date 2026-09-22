import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from browser_session import create_session
from token_provider import extract_csrf, extract_iframe_token
from vinfast_client import VinFastForgotPassword
from random_email import generate_emails
from report import save_report
import enumeration_test
import rate_limit_test

LOGIN_PAGE = (
    "https://shop.vinfastauto.com/"
    "vn_vi/login/iframe"
)

KNOWN_EMAIL = "hoangvn950@gmail.com"
RANDOM_COUNT = 10
DELAY_SECONDS = 1.5


def main():
    print("[1] Initializing session...")
    session = create_session()

    print("[2] Loading login iframe page...")
    response = session.get(LOGIN_PAGE, timeout=15)
    html = response.text

    print("[3] Extracting tokens...")
    csrf_token = extract_csrf(html)
    iframe_token = extract_iframe_token(html)

    if not csrf_token or not iframe_token:
        print("[-] Unable to extract required tokens. Stopping.")
        return

    print(f"[+] Token OK (CSRF len: {len(csrf_token)}, Iframe len: {len(iframe_token)})")

    client = VinFastForgotPassword(session=session)

    # 1 registered email + 10 random emails
    random_emails = generate_emails(RANDOM_COUNT)
    test_list = [
        {"email": KNOWN_EMAIL, "type": "registered"},
    ]
    for em in random_emails:
        test_list.append({"email": em, "type": "random_unregistered"})

    total_tests = len(test_list)
    results = []

    print(f"\n[4] Starting test suite ({total_tests} emails: 1 registered + {RANDOM_COUNT} random)...\n")

    registered_result = None

    for index, item in enumerate(test_list, start=1):
        email = item["email"]
        tag = item["type"]

        print(f"[{index}/{total_tests}] Testing [{tag}]: {email}")
        result = client.forgot_password(
            email=email,
            csrf_token=csrf_token,
            iframe_token=iframe_token,
        )
        result["type"] = tag
        results.append(result)

        if tag == "registered" and registered_result is None:
            registered_result = result

        time.sleep(DELAY_SECONDS)

    # Account Enumeration analysis
    enumeration_summary = {
        "tested_against_registered": KNOWN_EMAIL,
        "enumeration_issues_found": False,
        "details": [],
    }

    if registered_result:
        for res in results:
            if res["type"] == "random_unregistered":
                diff = enumeration_test.check(registered_result, res)
                if diff["issue"]:
                    enumeration_summary["enumeration_issues_found"] = True
                    enumeration_summary["details"].append({
                        "email": res["email"],
                        "reasons": diff["details"]
                    })

    # Rate Limiting analysis
    rate_limit_summary = rate_limit_test.analyze(results)

    final_report = {
        "target": "https://shop.vinfastauto.com",
        "endpoint": "Login-Auth0ForgotPassword",
        "total_requests": total_tests,
        "registered_email_tested": KNOWN_EMAIL,
        "random_emails_count": RANDOM_COUNT,
        "enumeration_analysis": enumeration_summary,
        "rate_limit_analysis": rate_limit_summary,
        "results": results,
    }

    print("\n[5] Saving test report...")
    save_report(final_report)
    print("[+] Test suite completed successfully!\n")


if __name__ == "__main__":
    main()