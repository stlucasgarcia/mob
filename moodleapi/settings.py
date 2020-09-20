"""
Settings module with variables already set
"""

from os import path


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
