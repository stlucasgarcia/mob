"""
Export Module contains only Export class to export any data to the Database
or csv file.

Last Update: 10/12/2020 - support for database export type

"""


import psycopg2
from psycopg2 import pool

from os import path
from pandas import DataFrame

from moodleapi.secret import DATABASE


class Export:
    """Export class has two types for export data, to the Database using
    information in secret1.py and to csv files."""

    def __init__(self, name=None):
        self.name = name
        self.path = path.abspath("bot").split("bot")[0] + f"csvfiles\{name}.csv"
        self.tpool, self.conn = Export._conn()

    def __str__(self):
        return f"Export object for file in path {self.path}"

    @staticmethod
    def _conn():
        try:
            threadedpool = psycopg2.pool.ThreadedConnectionPool(
                1,
                20,
                database=DATABASE["db"],
                user=DATABASE["user"],
                password=DATABASE["password"],
            )

            conn = threadedpool.getconn()

        except (Exception, psycopg2.DatabaseError) as err:
            raise ("Error while connecting to PostgreSQL", err)

        else:
            return threadedpool, conn

    def _create_table(self, *args, **kwargs):
        cursor = self.conn.cursor()

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
        self.tpool.putconn(self.conn)

    def to_csv(self, data=None, addstyle=True, *args, **kwargs):
        if data:
            df = DataFrame(data)
            df.to_csv(
                self.path,
                encoding="utf-8",
                index=False,
                header=False,
                mode="a" if addstyle else "w",
            )

        else:
            raise ValueError("Data not passed correctly. (type: list)")

    def to_db(self, data=None, *args, **kwargs):
        if data:
            moodle_db = ("moodle_events", "moodle_assign")

            cursor = self.conn.cursor()

            try:
                cursor.execute(f"SELECT 'public.{self.name}'::regclass")
                cursor.fetchall()
            except psycopg2.ProgrammingError:
                Export._create_table(self)

            if self.name in moodle_db:

                cursor.execute(
                    f"SELECT discord_id FROM {self.name} WHERE discord_id=%s AND guild_id=%s",
                    (data[0][0], data[0][1]),
                )
                exist = cursor.fetchall()

                if exist:
                    cursor.execute(
                        f"DELETE FROM public.{self.name} WHERE discord_id=%s AND guild_id=%s",
                        (data[0][0], data[0][1]),
                    )
                    self.conn.commit()

                for i in range(len(data)):
                    if kwargs["check"]:
                        query = (
                            f"INSERT INTO {self.name} (discord_id, guild_id, course, semester, class, subject, "
                            f"subject_name, description, subject_type, deadline, deadline_date, url, professor, "
                            f"status, submit_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )

                    else:
                        query = (
                            f"INSERT INTO {self.name} (discord_id, guild_id, course, semester, class, subject, "
                            f"subject_name, description, subject_type, deadline, deadline_date, url, professor)"
                            f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        )

                    cursor.execute(query, (*data[i],)[: 16 if kwargs["check"] else -2])
                    self.conn.commit()

            else:
                if self.name == "moodle_profile":
                    query = (
                        "INSERT INTO moodle_profile (discord_id, tia, course, semester, class, guild_id,"
                        " token) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                    )

                    try:
                        cursor.execute(query, (*data,))
                        self.conn.commit()

                    except psycopg2.IntegrityError as err:
                        print(f"Moodle Profile already exists.\n{err}\n")

                elif self.name == "moodle_professors":
                    cursor.execute(
                        "SELECT subject FROM moodle_professors "
                        "WHERE subject=$1 AND guild_id=$2",
                        data[0][3],
                        data[0][5],
                    )
                    exist = cursor.fetchall()

                    if exist:
                        cursor.execute(
                            "DELETE FROM public.moodle_professors "
                            "WHERE subject=$1 AND guild_id=$2",
                            data[0][3],
                            data[0][5],
                        )
                        self.conn.commit()

                    query = (
                        "INSERT INTO moodle_professors (course, semester, class, subject, "
                        "id, guild_id) VALUES (%s, %s, %s, %s, %s, %s)"
                    )

                    for i in range(len(data)):
                        cursor.execute(query, (*data[i],))
                        self.conn.commit()

                elif self.name == "bot_reminder":
                    cursor.execute(
                        "SELECT subject_name FROM bot_reminder "
                        "WHERE discord_id=%s AND guild_id=%s AND subject_name = %s",
                        (data[0], data[1], data[6]),
                    )
                    exist = cursor.fetchall()

                    if exist:
                        cursor.execute(
                            "DELETE FROM public.bot_reminder "
                            "WHERE discord_id=%s AND guild_id=%s AND subject_name = %s",
                            (data[0], data[1], data[6]),
                        )
                        self.conn.commit()

                    query = (
                        f"INSERT INTO bot_reminder (discord_id, guild_id, course, semester, class, subject, "
                        f"subject_name, description, subject_type, deadline, deadline_date, url, professor)"
                        f" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )

                    cursor.execute(query, (*data,))
                    self.conn.commit()

            cursor.close()
            self.tpool.putconn(self.conn)
            self.tpool.closeall()

        else:
            raise ValueError("Data or Database not passed correctly. (type: list, str)")
