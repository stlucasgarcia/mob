import psycopg2
from typing import Any


def db_exist(cursor: Any, tpool: Any, conn: Any, name: str) -> Any:
    try:
        cursor.execute(f"SELECT 'public.{name}'::regclass")
        cursor.fetchall()
    except psycopg2.ProgrammingError:
        create_table(cursor, tpool, conn)


def create_table(cursor, tpool, conn):
    cursor.execute(
        "CREATE TABLE moodle_events ("
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

    cursor.execute(
        "CREATE TABLE moodle_assign ("
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

    cursor.execute(
        "CREATE TABLE moodle_profile ("
        "discord_id numeric(18) PRIMARY KEY,"
        "tia varchar ,"
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "guild_id numeric(18),"
        "token varchar);"
    )

    cursor.execute(
        "CREATE TABLE moodle_professors ("
        "course varchar(3),"
        "semester varchar(2),"
        "class varchar(1),"
        "subject varchar,"
        "professor varchar,"
        "guild_id numeric(18));"
    )

    cursor.close()
    tpool.putconn(conn)


def events_check(
    cursor: Any,
    conn: Any,
    name: str,
    discord_id: int,
    guild_id: int,
) -> Any:
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
