import discord
from itertools import cycle

loop_channel = int(750313490455068722)

# Dictionary template that we use in most part of Moodle.py
def data_dict(i, database):
    assignmentsdata = { 
    "fullname" : database.iat[i,0].title(),
    "name" : database.iat[i,1].title(),
    "description" : database.iat[i,2],
    "modulename" : database.iat[i,3],
    "deadline" : database.iat[i,4].title() + " às " + database.iat[i,5].title(),
    "link" : database.iat[i, 6],
    "author" : str(database.iat[i, 7]).title(),
    "hwstatus" : database.iat[i, 8],
    "hwstatus_time" : database.iat[i, 9]
    }
    return assignmentsdata


def moodle_color(i, option, assignmentsdata):
    if option == "assignments":
        if i % 2 == 0: 
            color = 0x480006
        else:
            color = 0x9f000c

        return color


    elif option == "classes":
        if i % 2 == 0: 
            color = 0x29C8BA
        else:
            color = 0x155D56

        return color


    elif option == "events":
        if assignmentsdata["modulename"] == "Tarefa para entregar via Moodle":

            if i % 2 == 0: 
                color = 0x480006
            else:
                color = 0x9f000c

        else:

            if i % 2 == 0: 
                color = 0x29C8BA
            else:
                color = 0x155D56
                
        return color
