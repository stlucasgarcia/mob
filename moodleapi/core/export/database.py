from moodleapi.utils import db_query


def search_query(db: str) -> str:
    return eval(db_query[db] + "()")


def moodle_events_query():
    return (
        f"INSERT INTO moodle_events (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor)"
        f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_assign_query():
    return (
        f"INSERT INTO moodle_assign (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor, "
        f"status, submit_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_profile_query():
    return (
        "INSERT INTO moodle_profile (discord_id, tia, course, semester, class, guild_id,"
        " token) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_professors_query():
    return "INSERT INTO moodle_professors (course, semester, class, subject, guild_id) VALUES (%s, %s, %s, %s, %s)"


def bot_reminder_query():
    return (
        f"INSERT INTO bot_reminder (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor)"
        f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
