from discord import Embed
from utilities import thumbnail_url, defaultcolor, footer
from secret1 import bitly_token
import pyshorteners
import time

# Dictionary template that we use in most part of Moodle.py
def data_dict(database):
    assignmentsdata = {
        "fullname": database[5].title(),
        "name": database[6].title(),
        "description": database[7],
        "modulename": database[8],
        "deadline": database[9].title() + " às " + database[10].title(),
        "link": database[11],
        "author": str(database[12]).title(),
    }

    if len(database) > 13:
        assignmentsdata["hwstatus"] = database[13]
        assignmentsdata["hwstatus_time"] = database[14]

    return assignmentsdata


# Changing color for better student visualization
def moodle_color(i, assignmentsdata):
    if assignmentsdata["modulename"] == "Tarefa para entregar via Moodle":
        if i % 2 == 0:
            color = 0x480006
        else:
            color = 0x9F000C

        return color

    else:
        if i % 2 == 0:
            color = 0x29C8BA
        else:
            color = 0x155D56

        return color


# Styling the check command from moodle.py
def check_command_style(dict, amount="", color="", status=None, done=None):
    # Url shortener
    s = pyshorteners.Shortener(api_key=bitly_token)

    embed = Embed(
        title=dict["modulename"] + " - " + amount,
        color=color if color else defaultcolor,
    )
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Matéria", value=dict["fullname"], inline=True)
    embed.add_field(name="Nome da tarefa", value=dict["name"], inline=True)

    if status == 1:
        if dict["hwstatus"] == "Tarefa entregue":
            embed.set_author(
                name=dict["hwstatus"] + " " + dict["hwstatus_time"],
                icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Checkmark_green.svg/1200px-Checkmark_green.svg.png",
            )
            done += 1
        else:
            embed.set_author(
                name=dict["hwstatus"],
                icon_url="https://i1.pngguru.com/preview/326/505/102/red-cross-emoji-discord-logo-line-soviet-union-material-property-symbol-png-clipart.jpg",
            )

    if dict["description"] != "Descrição não disponível":
        if dict["description"].isspace():
            embed.add_field(
                name="Tipo de tarefa", value=dict["modulename"], inline=False
            )
        else:
            embed.add_field(name="Descrição", value=dict["description"], inline=False)
            embed.add_field(
                name="Tipo de tarefa", value=dict["modulename"], inline=True
            )
    else:
        embed.add_field(name="Tipo de tarefa", value=dict["modulename"], inline=False)

    if dict["modulename"] == "Aula ao vivo - BigBlueButton":
        embed.add_field(name="Data da aula", value=dict["deadline"], inline=True)
    else:
        embed.add_field(name="Data de entrega", value=dict["deadline"], inline=True)

    embed.add_field(name="Link", value=s.bitly.short(dict["link"]), inline=False)

    embed.add_field(name="Professor", value=dict["author"], inline=False)

    embed.set_footer(text=footer)
    return embed, done
