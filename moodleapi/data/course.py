"""
Course module specifically for course functions

Last Update: 10/12/2020 - support for contents and subjectsid function

"""

from moodleapi.request import Request


class Course(Request):
    """Course Class responsible to get all contents by courseid given
    that can be filtered by assignments for the time begin. Also, can
    get all subjects id by userid and professors name."""

    def __init__(self, token):
        super().__init__(token)

    def __str__(self):
        return "Course object"

    @staticmethod
    def filter(value=None, data=None, *args, **kwargs):
        """Disabled"""

        filtering = ""

        if value and data:
            pass

        else:
            raise ValueError(
                "Value or data parameter not passed correctly. (type: str, list)"
            )

    def contents(self, courseid=None, *args, **kwargs):
        if courseid:
            component = Request.get(
                self, wsfunction="core_course_get_contents", courseid=courseid
            )

            types_notallowed = ("assign", "bigbluebuttonbn", "forum", "chat", "label")

            data = []

            for week in component:
                for modules in week["modules"]:
                    if modules["modname"] not in types_notallowed:
                        data.append(
                            [
                                component[1]["modules"][0]["contents"][0]["author"],

                                week["name"],

                                modules["contents"][0]["type"],

                                modules["contents"][0]["filename"],

                                "%.2f KB"
                                % (int(modules["contents"][0]["filesize"]) / 8000)
                                if modules["contents"][0]["type"] == "file"
                                or modules["contents"][0]["filesize"] != "0 KB"
                                else 0,

                                modules["contents"][0]["fileurl"],
                            ]
                        )

            return data

        else:
            raise ValueError("Courseid not provided.")

    def simple_contents(self, courseid=None, instance=None, *args, **kwargs):
        if courseid and instance:
            events = Request.get(
                self, *args, wsfunction="core_course_get_contents", courseid=courseid
            )

            for modules in events:
                if modules["modules"]:
                    for module in modules["modules"]:
                        if module["id"] == instance:
                            return (
                                module["completiondata"]["state"],
                                module["completiondata"]["timecompleted"],
                            )

        else:
            raise ValueError("Courseid or Instance not provided. (type: int)")

    def get_subject_name(
        self, userid=None, *args, **kwargs
    ):  # TODO: REVISE IF IS NECESSARY
        if userid:
            subjects = Request.get(
                self, wsfunction="core_enrol_get_users_courses", userid=userid
            )

            subjects_notallowed = (5368, 9, 6854, 6937, 6801, 15331, 15338, 6858, 7885)

            for subject in subjects:
                if subject["id"] not in subjects_notallowed:
                    return subject["fullname"]

        else:
            raise ValueError("UserID not provided or Subject not allowed. (type: int)")

    def get_teacher(self, courseid=None, *args, **kwargs):
        if courseid:
            component = Request.get(
                self, wsfunction="core_course_get_contents", courseid=courseid
            )

            for section in component:
                for module in section["modules"]:

                    try:
                        if module["contents"][0]:
                            if module["contents"][0]["type"] == "file":
                                if module["contents"][0]["author"]:
                                    return module["contents"][0]["author"]

                    except (Exception, KeyError):
                        pass

            else:
                print(
                    "Unfortunately we couldn't find the teacher from this discipline."
                )
                return None

        else:
            raise ValueError("CourseID not provided. (type: int)")
