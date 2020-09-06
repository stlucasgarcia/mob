"""
Settings module with variables already set
"""


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
}

# Discipline dictionary



disc = {
    'ALGEBRA BOOLEANA E CIRC DIGITAIS [turma 02D] - 2020/2': 'Jamil Kalil NAUFAL JUNIOR'
}