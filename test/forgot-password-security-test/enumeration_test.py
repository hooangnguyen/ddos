import hashlib


def fingerprint(result):

    body = result.get(
        "body",
        {}
    )


    data = {

        "success":
            body.get("success"),

        "message":
            body.get("message")

    }


    return hashlib.sha256(

        str(data).encode()

    ).hexdigest()



def check(
    registered,
    unknown
):

    result = {

        "issue":
            False,

        "details":
            []

    }


    if fingerprint(
        registered
    ) != fingerprint(
        unknown
    ):

        result["issue"] = True

        result["details"].append(
            "Response khác nhau"
        )


    if (
        registered["body"].get("success")
        !=
        unknown["body"].get("success")
    ):

        result["issue"] = True

        result["details"].append(
            "Success flag khác nhau"
        )


    return result