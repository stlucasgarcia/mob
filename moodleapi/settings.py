"""
Settings module with variables already set
"""

import asyncpg, asyncio
from os import path


from moodleapi.secret import DATABASE


# Base config for connection with Moodle API

BASEURL = 'https://eadmoodle.mackenzie.br/'     # Url for any connection with the server
SERVICE = 'webservice/'                         # Type of service to connect with API (global)
API = 'rest/'                                   # Rest was added in 2.2 version of Moodle API
CONNECTION = 'server.php?'                      # Global prefix before any parameter
FORMAT = 'moodlewsrestformat=json'              # Setting json as response (specifically for rest)
TOKEN = '&wstoken='                             # Create prefix to token to be added when requested

REQUEST = f'{BASEURL}{SERVICE}{API}{CONNECTION}{FORMAT}{TOKEN}'


# Core Functions dictionary for suportted functions

func = {
    'calendar_monthly': 'core_calendar_get_calendar_monthly_view',
    'calendar_upcoming': 'core_calendar_get_calendar_upcoming_view',
    'calendar_day': 'core_calendar_get_calendar_day_view',

    'course_contents': 'core_course_get_contents',
    'course_subjects' : 'core_enrol_get_users_courses',
}


# TODO: CREATE FUNCTION FOR DISCIPLINE TEACHER AND ID DICTS
# Discipline teacher dictionary

data = []
with open(path.abspath('bot').split('bot')[0] + "csvfiles\professors.csv", 'r') as arq:
    for line in arq:
        line = line.split(',')
        line[1] = line[1][:-1]
        data.append(line)

professor = {k: v for k, v in data}

loop = asyncio.get_event_loop()

def professors(*args, **kwargs):

    async def names():
        conn = await asyncpg.create_pool(database=DATABASE['db'], user=DATABASE['user'],
                                         password=DATABASE['password'])

        exist = await conn.fetch("SELECT subject FROM moodle_professors "
                                 "WHERE subject=$1 AND guild_id=$2", data[0][3], data[0][5])

        if not exist:
            pass#Export('moode_professors').to_db(data=Course(kwargs['token']).get_subjects())

        query = "SELECT professor FROM moodle_professors WHERE course=$1 AND semester=$2 AND class=$3" \
                " AND subject=$4 AND guild_id=$5"

        values = kwargs['info']['course'], kwargs['info']['semester'], kwargs['info']['class'], \
                 kwargs['info']['subject'], kwargs['info']['guild_id']

        prof = [name for name in conn.execute(query, *values)]

        return prof

    return loop.run_until_complete(names())


# Discipline ID dictionary

data = []
with open(path.abspath('bot').split('bot')[0] + "csvfiles\subjectsid.csv", 'r') as arq:
    for line in arq:
        line = line.split(',')
        line[1] = line[1][:-1]
        data.append(line)

dict_id = {k: v for k, v in data}



# Month names to PT-BR
month = {
    'Jan': 'Janeiro',
    'Feb': 'Fevereiro',
    'Mar': 'Março',
    'Apr': 'Abril',
    'May': 'Maio',
    'Jun': 'Junho',
    'Jul': 'Julho',
    'Aug': 'Agosto',
    'Sep': 'Setembro',
    'Oct': 'Outubro',
    'Nov': 'Novembro',
    'Dec': 'Dezembro'
}


# Week day names to PT-BR
week = {
    'Sun': 'Domingo',
    'Mon': 'Segunda-feira',
    'Tue': 'Terça-feira',
    'Wed': 'Quarta-feira',
    'Thu': 'Quinta-feira',
    'Fri': 'Sexta-feira',
    'Sat': 'Sábado'
}
