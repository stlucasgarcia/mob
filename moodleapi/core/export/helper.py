import psycopg2
from typing import Any

from moodleapi.secret import DATABASE


def db_exist(name: str) -> None:
    conn = psycopg2.connect(**DATABASE)
    cursor = conn.cursor()

    cursor.execute(eval(f"create_{name}()"))

    conn.commit()
    cursor.close()
    conn.close()


def create_moodle_events() -> str:
    return (
        "CREATE TABLE IF NOT EXISTS moodle_events ("
        "discord_id numeric(18),"
        "guild_id numeric(18),"
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "subject varchar,"
        "subject_name varchar,"
        "description varchar,"
        "subject_type varchar,"
        "deadline varchar,"
        "deadline_date varchar,"
        "url varchar,"
        "professor varchar);"
    )


def create_moodle_assign() -> str:
    return (
        "CREATE TABLE IF NOT EXISTS moodle_assign ("
        "discord_id numeric(18),"
        "guild_id numeric(18),"
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "subject varchar,"
        "subject_name varchar,"
        "description varchar,"
        "subject_type varchar,"
        "deadline varchar,"
        "deadline_date varchar,"
        "url varchar,"
        "professor varchar,"
        "status varchar,"
        "submit_date varchar);"
    )


def create_moodle_professor() -> str:
    return (
        "CREATE TABLE IF NOT EXISTS moodle_professors ("
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "subject varchar,"
        "professor varchar,"
        "guild_id numeric(18));"
    )


def create_moodle_profile() -> str:
    return (
        "CREATE TABLE IF NOT EXISTS moodle_profile ("
        "discord_id numeric(18) PRIMARY KEY,"
        "tia varchar ,"
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "guild_id numeric(18),"
        "token varchar);"
    )


def events_check(
    cursor: Any,
    conn: Any,
    name: str,
    discord_id: int,
    guild_id: int,
) -> None:
    cursor.execute(
        f"SELECT discord_id FROM {name} WHERE discord_id=%s AND guild_id=%s",
        (discord_id, guild_id),
    )
    exist = cursor.fetchall()

    if exist:
        cursor.execute(
            f"DELETE FROM public.{name} WHERE discord_id=%s AND guild_id=%s",
            (discord_id, guild_id),
        )
        conn.commit()


def profile_check(
    cursor: Any,
    conn: Any,
    name: str,
) -> Any:
    pass


def professors_check(
    cursor: Any,
    conn: Any,
    name: str,
) -> Any:
    pass


def reminder_check(
    cursor: Any,
    conn: Any,
    name: str,
) -> Any:
    pass
