import json


def save_report(data):

    with open(
        "report.json",
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(

            data,

            f,

            indent=4,

            ensure_ascii=False

        )


    print(
        "[+] Report saved: report.json"
    )