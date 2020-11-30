from requests import Session

from moodleapi.core.calendar import clean


def get_user_profile(**kwargs):
    """Used to get the moodle profile through the email"""

    r = Session()

    params = {
        "wstoken": kwargs["token"],
        "wsfunction": "core_user_get_users_by_field",
        "moodlewsrestformat": "json",
        "field": "email",
        "values[0]": kwargs["tia"] + "@mackenzista.com.br",
    }

    data = r.get(kwargs["url"], params=params, stream=True).json()
    data[0]["description"] = clean(data[0]["description"])

    return data[0]
