import discord
from itertools import cycle


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