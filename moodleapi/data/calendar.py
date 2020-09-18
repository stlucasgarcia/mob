"""
Calendar module especifically for calendar functions

Last Update: 09/18/2020 - added new filters for events
"""

from moodleapi.request import Request
from moodleapi.settings import professor, week, month
from moodleapi.data.course import Course

from datetime import datetime as dt
from re import compile, sub


class Calendar(Request):
    """Calendar Class support montlhy informations only and have
    several functions to filter information and format date."""

    def __init__(self, token):
        self.token = token
        super().__init__(token)


    def __str__(self):
        return 'Calendar object'


    def _clean(self, value):
         return sub(compile('<.*?>'), '', value)


    def _time(self, epoch):
        from time import ctime

        date = ctime(epoch).split()

        return f'{week[date[0]]}, {date[2]} de {month[date[1]]} às {date[3][:-3]}'


    def _check_time(self, current_h, current_m, assign_h, assign_m, today):
        if current_h > assign_h and today:
            return False
        elif current_h == assign_h and today:
            return False if current_m > assign_m else True
        else:
            return True


    def _verify(self, courseid, instance):
        co = Course(self.token)
        data =  co.contents(courseid=courseid, assign=True)
        filtered = co.filter(value=instance, data=data)

        return filtered


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

        d, h, m = dt.today().day, dt.today().hour, dt.today().minute


        allowed_modules = ('assign', 'bigbluebuttonbn')
        courses_notallowed = ('ALGORITMOS E PROGRAMACAO I [turma 01G] - 2020/2',)


        data = []

        for week in month:
            for day in week['days']:
                for events in day['events']:

                    period = True if d <= int(day['mday']) < d + 15 else False
                    today = True if day['mday'] == d else False

                    deadline = Calendar._clean(self, events['formattedtime'])[:-2] \
                        if events['modulename'] in allowed_modules else None

                    up_to_date = Calendar._check_time(self, h, m, int(deadline[:2]), int(deadline[3:5]), today) \
                        if deadline else True


                    if events['modulename'] in allowed_modules and events['course']['fullname'] \
                            not in courses_notallowed and period and up_to_date:


                        status, time = None, None
                        if events['modulename'] == 'assign':
                            status, time = Calendar._verify(self, events['course']['id'], events['instance'])


                        data.append([

                            events['course']['fullname'],

                            events['name'].split(' is ')[0] if ' is ' in events['name']
                            else events['name'].split(' está ')[0],

                            Calendar._clean(self, events['description']) if events['description'] != ''
                            else 'Descrição não disponível',

                            'Aula ao vivo - BigBlueButton' if events['modulename'] == 'bigbluebuttonbn' else
                            'Tarefa para entregar via Moodle',

                            day['popovertitle'].split(' eventos')[0],

                            deadline,

                            events['url'],

                            professor[f'{events["course"]["fullname"]}'],

                            f'Tarefa {"não " if status == 0 or not status else ""}entregue',

                            Calendar._time(self, time) if time != 0 and time else ''

                        ])

        return data
