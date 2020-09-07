"""
Calendar module especifically for calendar funcitons

Last Update: 05/09/2020 - support for calendar_monthly
"""

from moodleapi.request import Request

from datetime import datetime as dt
from re import compile, sub


class Calendar(Request):

    def __init__(self, token):
        super().__init__(token)


    def __str__(self):
        return 'Calendar object'


    def _clean(self, value):
         return sub(compile('<.*?>'), '', value)


    def filter(self, value=None, data=None, *args, **kwargs):
        filtering = 'Aula ao vivo - BigBlueButton' if value == 'bbb' else 'Tarefa para entregar via Moodle'

        if value and data:
            filtered = []

            for row in data:
                if row[3] == filtering:
                    filtered.append(row)

            return filtered

        else:
            raise ValueError('Value or data parameter not passed correctly.')


    def monthly(self, month=str(dt.today().month), year=str(dt.today().year), *args, **kwargs):
        month = Request.get(self, function='core_calendar_get_calendar_monthly_view', year=year, month=month)['weeks']

        data = []

        for week in month:
            for day in week['days']:
                for events in day['events']:
                    if (events['modulename'] == 'assign' or events['modulename'] == 'bigbluebuttonbn')\
                            and events['course']['fullname'] != 'ALGORITMOS E PROGRAMACAO I [turma 01G] - 2020/2':
                        data.append(
                            [
                                events['course']['fullname'],
                                events['name'],

                                Calendar._clean(self, events['description']) if events['description'] != ''
                                else 'Descrição não disponível',

                                'Aula ao vivo - BigBlueButton' if events['modulename'] == 'bigbluebuttonbn' else
                                'Tarefa para entregar via Moodle',

                                day['popovertitle'][:len(day['popovertitle']) - 8],

                                events['formattedtime'].split(':')[0][::-1][0:2][::-1] + ':'
                                + events['formattedtime'].split(':')[1][0:2],

                                events['url'],


                            ]
                        )

        return data
