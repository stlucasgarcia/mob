from requests import Session

from moodleapi.core.calendar import clean


class MoodleProfile:
    """Class created to organize the moodle profile request"""

    def __init__(self):
        self.r = Session()

    def get_user_profile_data(self, **kwargs) -> dict:
        """Used to get the moodle profile through the email(tia)"""

        params = {
            "wstoken": kwargs["token"],
            "wsfunction": "core_user_get_users_by_field",
            "moodlewsrestformat": "json",
            "field": "email",
            "values[0]": kwargs["tia"]
            + "@mackenzista.com.br",  # TODO Make it available to other Moodle in the future
        }
        username = self.r.get(kwargs["url"], params=params, stream=True).json()

        if not username:
            print("Invalid Username/params - moodleapi.core.profile")
            return

        params = {
            "wstoken": kwargs["token"],
            "wsfunction": "core_user_get_course_user_profiles",
            "userlist[0][userid]": username[0]["id"],
            "userlist[0][courseid]": 1,
            "moodlewsrestformat": "json",
        }

        data = self.r.get(kwargs["url"], params=params, stream=True).json()

        data[0]["description"] = clean(data[0]["description"])

        return data[0]
