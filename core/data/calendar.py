"""
Calendar module especifically for calendar funcitons

Last Update: 05/09/2020 - support for calendar_monthly
"""

from os.path import abspath
from pandas import DataFrame

from core.request import Request
from core.token import Token


class Export(Request, Token):

    def __init__(self, token):
        super().__init__(token)
        self.path = abspath('template.csv')


    def writeFunc(self, name=None, data=None, *args, **kwargs):
        if name and data:
            df = DataFrame(data)
            df.to_csv(self.path, encoding='utf-8', index=False, header=False)

        else:
            return 'File name or data list not passed.'


    def getToken(self, *args, **kwargs):
        token = Token.post(self, username='', password='')


    def getCalendarMonthly(self, *args, **kwargs):
        month = Request.get(self, function='core_calendar_get_calendar_monthly_view', year='2020', month='9')['weeks']

        data = []

        for week in month:
            for day in week['days']:
                for events in day['events']:
                    if events['modulename'] == 'assign' or events['modulename'] == 'bigbluebuttonbn':
                        data.append(
                            [
                                events['course']['fullname'],
                                events['name'],
                                events['description'],

                                events['modulename'][:len(events['modulename'])-2]
                                if events['modulename'] == 'bigbluebuttonbn' else events['modulename'],

                                day['popovertitle'][:len(day['popovertitle']) - 8],

                                events['formattedtime'].split(':')[0][::-1][0:2][::-1] + ':'
                                + events['formattedtime'].split(':')[1][0:2],

                                events['url'],
                            ]
                        )

        Export.writeFunc(self, name='template.csv', data=data)
