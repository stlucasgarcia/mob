"""
Settings module with variables already set
"""


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

# Month names translated to PT-BR
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


# Week day names translated to PT-BR
week = {
    'Sun': 'Domingo',
    'Mon': 'Segunda-feira',
    'Tue': 'Terça-feira',
    'Wed': 'Quarta-feira',
    'Thu': 'Quinta-feira',
    'Fri': 'Sexta-feira',
    'Sat': 'Sábado'
}
