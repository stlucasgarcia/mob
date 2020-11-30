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
    data["description"] = clean(data["description"])

    return data


dict = {
    "token": "8c745a73b1836bccf43619a99b1f013c",
    "tia": "32074956",
    "url": "https://eadmoodle.mackenzie.br/webservice/rest/server.php?",
}

print(get_user_profile(**dict))