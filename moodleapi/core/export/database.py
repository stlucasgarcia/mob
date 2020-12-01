def search_query(db: str) -> str:
    return eval(f"{db}_query()")


def moodle_events_query():
    """Returns the query for the moodle events table"""

    return (
        f"INSERT INTO moodle_events (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_assign_query():
    """Returns the query for the moodle assign table"""

    return (
        f"INSERT INTO moodle_assign (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor, "
        f"status, submit_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_profile_query():
    """Returns the query for the moodle profile table"""

    return (
        "INSERT INTO moodle_profile (discord_id, tia, course, semester, class, guild_id, token) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    )


def moodle_professors_query():
    """Returns the query for the moodle professors table"""

    return (
        "INSERT INTO moodle_professors (course, semester, class, subject, guild_id) "
        "VALUES (%s, %s, %s, %s, %s)"
    )


def bot_reminder_query():
    """Returns the query for the bot reminder table"""

    return (
        f"INSERT INTO bot_reminder (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    )
