"""
Professor module responsable to get informations about professor's

Last Update: 10/12/2020 - create Professor class and get method

"""


import psycopg2
from psycopg2 import pool

from moodleapi.data.course import Course
from moodleapi.secret import DATABASE


class Professor:
    """Professor class has an often function to get professor name
    by the courseid given."""

    @staticmethod
    def get(*args, **kwargs):
        threadedpool = psycopg2.pool.ThreadedConnectionPool(1, 20, database=DATABASE['db'], user=DATABASE['user'],
                                                            password=DATABASE['password'])

        conn = threadedpool.getconn()
        cursor = conn.cursor()

        cursor.execute("SELECT professor FROM moodle_professors WHERE course=%s AND subject=%s AND guild_id=%s",
                       (kwargs['course'], kwargs['subject'], kwargs['guild_id']))
        exist = cursor.fetchall()

        if not exist:
            prof = Course(kwargs['token']).get_teacher(courseid=kwargs['courseid'])

            cursor.execute("INSERT INTO moodle_professors (course, semester, class, subject, professor, guild_id) "
                           "VALUES (%s, %s, %s, %s, %s, %s)", (kwargs['course'], kwargs['semester'], kwargs['class'],
                                                               kwargs['subject'], prof, kwargs['guild_id']))
            conn.commit()

            cursor.close()
            threadedpool.putconn(conn)
            threadedpool.closeall()

            return prof

        cursor.close()
        threadedpool.putconn(conn)
        threadedpool.closeall()

        return exist[0]