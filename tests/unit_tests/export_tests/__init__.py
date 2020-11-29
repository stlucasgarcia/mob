query_dict = {
    "moodle_events_query": (
        f"INSERT INTO moodle_events (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ),
    "moodle_assign_query": (
        f"INSERT INTO moodle_assign (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor, "
        f"status, submit_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ),
    "moodle_profile_query": (
        "INSERT INTO moodle_profile (discord_id, tia, course, semester, class, guild_id, token) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
    ),
    "moodle_professors_query": (
        "INSERT INTO moodle_professors (course, semester, class, subject, guild_id) "
        "VALUES (%s, %s, %s, %s, %s)"
    ),
    "bot_reminder_query": (
        f"INSERT INTO bot_reminder (discord_id, guild_id, course, semester, class, subject, "
        f"subject_name, description, subject_type, deadline, deadline_date, url, professor) "
        f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    ),
}


__all__ = [
    "query_dict",
]
