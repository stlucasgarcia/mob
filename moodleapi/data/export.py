"""
Export Module contains only Export class to export any data for an
csv file passed.
"""


import asyncpg, asyncio
from os import path
from pandas import DataFrame

from moodleapi.secret import DATABASE


class Export:

    def __init__(self, name=None):
        super().__init__()
        self.name = name
        self.path = path.abspath('bot').split('bot')[0] + f"csvfiles\{name}.csv"


    def __str__(self):
        return f'Export object for file in path {self.path}'


    def _create_table(self, *args, **kwargs):
        async def create():
            conn = await asyncpg.create_pool(database=DATABASE['db'], user=DATABASE['user'],
                                             password=DATABASE['password'])

            await conn.execute("CREATE TABLE moodle_events ("
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
                         "professor varchar);")

            await conn.execute("CREATE TABLE moodle_assign ("
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
                         "submit_date varchar);")

            await conn.execute("CREATE TABLE moodle_profile ("
                         "discord_id numeric(18) PRIMARY KEY,"
                         "tia varchar ,"
                         "course varchar(3),"
                         "semester varchar(2),"
                         "class varchar(1),"
                         "guild_id numeric(18),"
                         "token varchar);")

            await conn.execute("CREATE TABLE moodle_professors ("
                               "course varchar(3),"
                               "semester varchar(2),"
                               "class varchar(1),"
                               "subject varchar,"
                               "professor varchar,"
                               "guild_id numeric(18));")

            conn.close()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(create())
        loop.close()


    def to_csv(self, data=None, addstyle=True, *args, **kwargs):
        if data:
                df = DataFrame(data)
                df.to_csv(self.path, encoding='utf-8', index=False, header=False,
                          mode='a' if addstyle else 'w')

        else:
            raise ValueError('Data not passed correctly. (type: list)')


    def to_db(self, data=None, *args, **kwargs):
        if data:
            moodle_db = ('moodle_events', 'moodle_assign')

            async def export():
                conn = await asyncpg.create_pool(database=DATABASE['db'], user=DATABASE['user'], password=DATABASE['password'])

                try:
                    await conn.execute(f"SELECT 'public.{self.name}'::regclass")
                except asyncpg.exceptions.UndefinedTableError:
                    return True


                if self.name in moodle_db:

                    exist = await conn.fetch(f"SELECT discord_id FROM {self.name} WHERE discord_id=$1 AND guild_id=$2",
                                             data[0][0], data[0][1])

                    if exist:
                        await conn.execute(f"DELETE FROM public.{self.name} WHERE discord_id=$1 AND guild_id=$2",
                                           data[0][0], data[0][1])

                    st = f", status, submit_date" if kwargs['check'] else ''
                    pp = ', $14, $15' if st else ''

                    query = f"INSERT INTO {self.name} (discord_id, guild_id, course, semester, class, subject, subject_name," \
                            f" description, subject_type, deadline, deadline_date, url, professor{st}) VALUES" \
                            f" ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13{pp});"

                    for row in data:
                        values = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9],
                                  row[10], row[11], row[12]]

                        if pp:
                            values.append(row[13])
                            values.append(row[14])

                        await conn.execute(query, *values)

                else:
                    if self.name == 'moodle_profile':
                        print(data)
                        query = "INSERT INTO moodle_profile (discord_id, tia, course, semester, class, guild_id," \
                                " token) VALUES ($1, $2, $3, $4, $5, $6, $7)"

                        values = data[0], data[1], data[2], data[3], data[4], data[5], data[6]

                        try:
                            await conn.execute(query, *values)

                        except: #TODO: add execpt error
                            raise asyncpg.exceptions.InvalidForeignKeyError('Moodle Profile already exists.')

                    elif self.name == 'moodle_professors':
                        exist = await conn.fetch("SELECT subject FROM moodle_professors "
                                                 "WHERE subject=$1 AND guild_id=$2", data[0][3], data[0][5])

                        if exist:
                            await conn.execute("DELETE FROM public.moodle_professors "
                                               "WHERE subject=$1 AND guild_id=$2", data[0][3], data[0][5])

                        query = "INSERT INTO moodle_professors (course, semester, class, subject, " \
                                "id, guild_id) VALUES ($1, $2, $3, $4, $5, $6)"

                        for row in data:
                            values = row[0], row[1], row[2], row[3], row[4], row[5]

                            await conn.execute(query, *values)

                conn.close()

            loop = asyncio.get_event_loop()
            created = loop.run_until_complete(export())

            if created:
                Export._create_table(self)
                loop.run_until_complete(export())

            loop.close()


        else:
            raise ValueError('Data or Database not passed correctly. (type: list, str)')
