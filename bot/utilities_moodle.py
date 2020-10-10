import discord
from itertools import cycle

loop_channel = int(750313490455068722)

# Dictionary template that we use in most part of Moodle.py
def data_dict(database):
    assignmentsdata = { 
    "fullname" : database[5].title(),
    "name" : database[6].title(),
    "description" : database[7],
    "modulename" : database[8],
    "deadline" : database[9].title() + " às " + database[10].title(),
    "link" : database[11],
    "author" : str(database[12]).title(),
    #"hwstatus" : database[13] if database[13] else '',
    #"hwstatus_time" : database[14] if database[14] else ''
    }
    return assignmentsdata


# Changing color for better student visualization
def moodle_color(i, assignmentsdata):
    if assignmentsdata["modulename"] == "Tarefa para entregar via Moodle":
        if i % 2 == 0: 
            color = 0x480006
        else:
            color = 0x9f000c

        return color

    else:
        if i % 2 == 0: 
            color = 0x29C8BA
        else:
            color = 0x155D56

        return color

