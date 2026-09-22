import random
import string


FIRST_NAMES = [

    "anh",
    "minh",
    "nam",
    "hung",
    "tuan",
    "long",
    "linh",
    "hoa",
    "ngoc",
    "mai"

]


LAST_NAMES = [

    "nguyen",
    "tran",
    "le",
    "pham",
    "do",
    "vu",
    "hoang"

]


def random_email():

    first = random.choice(
        FIRST_NAMES
    )

    last = random.choice(
        LAST_NAMES
    )


    number = "".join(

        random.choices(
            string.digits,
            k=4
        )

    )


    return (
        f"{first}.{last}{number}"
        "@gmail.com"
    )



def generate_emails(count=10):

    emails = []

    for _ in range(count):

        emails.append(
            random_email()
        )


    return emails