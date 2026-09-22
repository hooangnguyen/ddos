import hashlib


def fingerprint(result):
    body = result.get("response") or result.get("body", {})

    data = {
        "success": body.get("success"),
        "message": body.get("message"),
        "action": body.get("action"),
    }

    return hashlib.sha256(
        str(data).encode()
    ).hexdigest()



def check(
    registered,
    unknown
):
    result = {
        "issue": False,
        "details": []
    }

    if fingerprint(registered) != fingerprint(unknown):
        result["issue"] = True
        result["details"].append("Response payload differs")

    reg_body = registered.get("response") or registered.get("body", {})
    unk_body = unknown.get("response") or unknown.get("body", {})

    if reg_body.get("success") != unk_body.get("success"):
        result["issue"] = True
        result["details"].append("Success flag differs")

    return result