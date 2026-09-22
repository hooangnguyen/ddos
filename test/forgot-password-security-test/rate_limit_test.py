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

        code = item["status"]


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