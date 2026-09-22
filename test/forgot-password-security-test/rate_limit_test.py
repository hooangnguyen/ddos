import time


def analyze(results):

    report = {

        "total":
            len(results),

        "status_codes":
            {},

        "rate_limit_detected":
            False

    }


    for item in results:
        code = item.get("status_code") or item.get("status", 0)


        report["status_codes"][code] = (

            report["status_codes"]
            .get(code, 0)
            + 1

        )


        if code == 429:

            report[
                "rate_limit_detected"
            ] = True


    return report