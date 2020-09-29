"""
Course module especifically for course functions

Last Update: 09/18/2020 - support for contents and subjectsid function
"""

from moodleapi.request import Request


class Course(Request):
    """Course Class responsable to get all contents by courseid given
    that can be filtered by assingments for the time beign. Also, can
    get all subjects id by userid."""

    def __init__(self, token):
        super().__init__(token)


    def __str__(self):
        return 'Course object'


    def filter(self, value=None, data=None, *args, **kwargs):
        """Disabled"""

        filtering = ''

        if value and data:
            pass

        else:
            raise ValueError('Value or data parameter not passed correctly. (type: str, list)')


    def contents(self, courseid=None, *args, **kwargs):
        if courseid:
            component = Request.get(self, wsfunction='core_course_get_contents', courseid=courseid)

            types_notallowed = ('assign', 'bigbluebuttonbn', 'forum', 'chat', 'label')

            data = []

            for week in component:
                for modules in week['modules']:
                    if modules['modname'] not in types_notallowed:
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

            return data


        else:
            raise ValueError('Courseid not provided.')


    def simple_contents(self, courseid=None, instance=None, *args, **kwargs):
        if courseid and instance:
            events = Request.get(self, *args, wsfunction='core_course_get_contents', courseid=courseid)

            for modules in events:
                if modules['modules']:
                    for module in modules['modules']:
                        if module['id'] == instance:
                            return module['completiondata']['state'], module['completiondata']['timecompleted']


        else:
            raise ValueError('Courseid or Instance not provided. (type: int)')


    def get_subjects(self, userid=None, *args, **kwargs):
        if userid:
            subjects = Request.get(self, wsfunction='core_enrol_get_users_courses', userid=userid)

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
