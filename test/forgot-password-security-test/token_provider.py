# token_provider.py

import re


def extract_value(
    html,
    field_name
):

    patterns = [

        # input hidden
        rf'name="{field_name}".*?value="(.*?)"',

        # value trước name
        rf'value="(.*?)".*?name="{field_name}"',

        # javascript object
        rf'{field_name}["\']?\s*:\s*["\'](.*?)["\']'

    ]


    for pattern in patterns:

        result = re.search(
            pattern,
            html,
            re.S
        )


        if result:

            return result.group(1)


    return None



def extract_csrf(html):

    return extract_value(
        html,
        "csrf_token"
    )



def extract_iframe_token(html):

    return extract_value(
        html,
        "iframeLoginToken"
    )