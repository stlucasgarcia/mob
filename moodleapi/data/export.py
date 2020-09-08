"""
Export Module contains only Export class to export any data for an
csv file passed.
"""


from os import path
from pandas import DataFrame


class Export:

    def __init__(self, name=None):
        super().__init__()
        self.path = path.abspath('bot').split('bot')[0] + f"csvfiles\{name}.csv"


    def __str__(self):
        return f'Export object for file in path {self.path}'


    def to_csv(self, data=None, addstyle=True, *args, **kwargs):
        if data:
                df = DataFrame(data)
                df.to_csv(self.path, encoding='utf-8', index=False, header=False,
                          mode='a' if addstyle else 'w')

        else:
            raise ValueError('Data not passed correctly. (type: list)')
