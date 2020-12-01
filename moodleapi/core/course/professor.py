from typing import Any


def get_professor(cursor: Any, conn: Any, **kwargs) -> str:
    """This function is responsible for getting the user's professor in the database which is used to check the status of assignments"""

    cursor.execute(
        "SELECT professor FROM moodle_professors WHERE course=%s AND subject=%s AND guild_id=%s",
        (kwargs["course"], kwargs["subject"], kwargs["guild_id"]),
    )
    exist = cursor.fetchall()
    prof = "Professor não encontrado"

    if not exist:
        params = {
            "wsfunction": "core_course_get_contents",
            "wstoken": kwargs["token"],
            "courseid": kwargs["courseid"],
            "options[0][name]": "modname",
            "options[0][value]": "resource",
            "moodlewsrestformat": "json",
        }
        prof = _find_professor(
            kwargs["r"].get(kwargs["url"], params=params, stream=True).json()
        )

        cursor.execute(
            "INSERT INTO moodle_professors (course, semester, class, subject, professor, guild_id) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (
                kwargs["course"],
                kwargs["semester"],
                kwargs["class"],
                kwargs["subject"],
                prof,
                kwargs["guild_id"],
            ),
        )

    else:
        prof = exist[0]

    conn.commit()
    return prof


def _find_professor(data: dict) -> str:
    for modules in data:
        for module in modules["modules"]:
            if module["contents"]:
                if module["contents"][0]["author"]:
                    return module["contents"][0]["author"]
