from requests import Session

from moodleapi.core.calendar import clean


class MoodleProfile:
    """Class created to organize the moodle profile request"""

    def __init__(self):
        self.r = Session()

    def get_user_profile(self, **kwargs) -> dict:
        """Used to get the moodle profile through the email(tia)"""

        params = {
            "wstoken": kwargs["token"],
            "wsfunction": "core_user_get_users_by_field",
            "moodlewsrestformat": "json",
            "field": "email",
            "values[0]": kwargs["tia"] + "@mackenzista.com.br",
        }
        data = self.r.get(kwargs["url"], params=params, stream=True).json()

        if not data:
            print("Invalid Username/params - moodleapi.core.profile")
            return

        data[0]["description"] = clean(data[0]["description"])

        return data[0]
