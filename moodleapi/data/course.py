"""
Course module ...
"""

from moodleapi.request import Request


class Course(Request):

    def __init__(self, token):
        super().__init__(token)


    def __str__(self):
        return 'Course object'


    def filter(self, value=None, data=None, *args, **kwargs):
        filtering = ''

        if value and data:

            for component in data:
                    if component[0] == value:

                        return component[1], component[2]

        else:
            raise ValueError('Value or data parameter not passed correctly. (type: str and list)')



    def contents(self, courseid=None, assign=False, *args, **kwargs):
        if courseid:
            component = Request.get(self, function='core_course_get_contents', courseid=courseid)

            types_notallowed = ('assign', 'bigbluebuttonbn', 'forum', 'chat', 'label')

            data = []

            for week in component:
                for modules in week['modules']:
                    if modules['modname'] not in types_notallowed and not assign:
                        data.append([
                            component[1]['modules'][0]['contents'][0]['author'],

                            week['name'],

                            modules['contents'][0]['type'],

                            modules['contents'][0]['filename'],

                            '%.2f KB' % (int(modules["contents"][0]["filesize"])/8000) \
                                if modules['contents'][0]['type'] == 'file' \
                                or modules['contents'][0]['filesize'] != '0 KB' else 0,

                            modules['contents'][0]['fileurl'],

                        ])


                    elif modules['modname'] == 'assign' and assign:
                        data.append([
                            modules['id'],

                            modules['completiondata']['state'],

                            modules['completiondata']['timecompleted'],
                        ])

            return data

        else:
            raise ValueError('Courseid not provided.')


    def get_subjects(self, userid=None, *args, **kwargs):
        if userid:
            subjects = Request.get(self, function='core_enrol_get_users_courses', userid=userid)

            subjects_notallowed = (5368, 9, 6854, 6937, 6801, 15331, 15338, 6858, 7885)

            data = []

            for subject in subjects:
                if subject['id'] not in subjects_notallowed:
                    data.append([
                        subject['fullname'],

                        subject['id'],
                    ])


            return data

        else:
            raise ValueError('UserID not provided or Subject not allowed. (type: int)')