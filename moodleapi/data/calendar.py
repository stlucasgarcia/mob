"""
Calendar module especifically for calendar funcitons

Last Update: 05/09/2020 - support for calendar_monthly
"""

from moodleapi.request import Request
from moodleapi.settings import professor, week, month
from moodleapi.data.course import Course

from datetime import datetime as dt
from re import compile, sub


class Calendar(Request):

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
                    deadline = Calendar._clean(self, events['formattedtime']) if events['modulename'] in allowed_modules else -1

                    #print(deadline)
                    #print(h < (int(deadline[:2]) if int(deadline[:2]) != 0 else 24))
                    #hourlimit = False if (h < (int(deadline[:2]) if int(deadline[:2]) != 0 else 24)) else True
                    #minutelimit = m < int(deadline[4:6]) if hourlimit else False

                    if events['modulename'] in allowed_modules and events['course']['fullname'] not in courses_notallowed \
                            and period: #and (today and (not hourlimit and minutelimit)):
                        #print(not hourlimit, minutelimit)

                        status, time = None, None
                        if events['modulename'] == 'assign':
                            status, time = Calendar._verify(self, events['course']['id'], events['instance'])

                        data.append(
                            [
                                events['course']['fullname'],

                                events['name'].split(' is ')[0] if ' is ' in events['name']
                                else events['name'].split(' está ')[0],

                                Calendar._clean(self, events['description']) if events['description'] != ''
                                else 'Descrição não disponível',

                                'Aula ao vivo - BigBlueButton' if events['modulename'] == 'bigbluebuttonbn' else
                                'Tarefa para entregar via Moodle',

                                day['popovertitle'].split(' eventos')[0],

                                deadline[:-2],

                                events['url'],

                                professor[f'{events["course"]["fullname"]}'],

                                f'Tarefa {"não " if status == 0 else ""}entregue',

                                Calendar._time(self, time) if time != 0 else ''

                            ]
                        )

        return data
