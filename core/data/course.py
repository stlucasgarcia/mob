"""
Course module ...
"""

from core.request import Request


class Course(Request):

    def __init__(self, token):
        super().__init__(token)


    def __str__(self):
        return 'Course object'


    def filter(self, value=None, data=None, *args, **kwargs):
        filtering = ''

        if value and data:
            pass

        else:
            raise ValueError('Value or data parameter not passed correctly.')



    def contents(self, courseid=None, *args, **kwargs):
        if courseid:
            component = Request.get(self, function='core_course_get_contents', courseid=courseid)
            #[0]['modules'][0]['contents'][0]['author']

            data = []

            data.append(component['modules']['contents']['author'])
            for section in component:
                act = [section['name']]
                for modules in section:
                    pass


            return

        else:
            raise ValueError('Courseid not provided.')