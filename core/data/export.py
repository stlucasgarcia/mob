"""
Export Module contains only Export class to export any data for an
csv file passed.
"""

from core.token import Token

from os import path
from pandas import DataFrame


class Export(Token):

    def __init__(self, name=None):
        super().__init__()
        self.path = path.join(path.abspath('bot')[:-3], path.abspath(f'csvfiles\{name}'))
        print(self.path)


    def __str__(self):
        return f'Export object for file in path {self.path}'


    def to_csv(self, data=None, *args, **kwargs):
        if data:
            df = DataFrame(data)
            df.to_csv(self.path, encoding='utf-8', index=False, header=False)

        else:
            raise ValueError('Data list not passed correctly.')