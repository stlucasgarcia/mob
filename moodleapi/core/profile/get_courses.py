from requests import Session


class MoodleCourse:
    """Class created to organize the moodle courses request"""

    def __init__(self):
        self.r = Session()

    def get_user_courses(self, **kwargs) -> list:

        params = {
            "wstoken": kwargs["token"],
            "wsfunction": "core_enrol_get_users_courses",
            "moodlewsrestformat": "json",
            "userid": kwargs["user_id"],
        }

        data = self.r.get(kwargs["url"], params=params, stream=True).json()

        if not data:
            print("Invalid user_id/params - moodleapi.core.get_user_courses")
            return

        return data
