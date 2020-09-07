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
TOKEN = '&wstoken='                              # Create prefix to token to be added when requested

REQUEST = f'{BASEURL}{SERVICE}{API}{CONNECTION}{FORMAT}{TOKEN}'


# Core Functions dictionary for suportted functions

func = {
    'calendar_monthly': 'core_calendar_get_calendar_monthly_view',
    'course_contents': 'core_course_get_contents',
    'course_subjects' : 'core_enrol_get_users_courses',
}


# Discipline teacher dictionary

teacher = {
    'ALGEBRA BOOLEANA E CIRC DIGITAIS [turma 02D] - 2020/2': 'JAMIL KALIL NAUFAL JUNIOR',
}


# Discipline ID dictionary

data = []
with open(path.join(path.abspath('bot')[:-3], path.abspath('csvfiles\subjectsid.csv')), 'r') as arq:
    for line in arq:
        line = line.split(',')
        line[1] = line[1][:-1]
        data.append(line)

dict_id = {k: v for k, v in data}