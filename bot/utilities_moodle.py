from discord import Embed
from utilities import thumbnail_url, defaultcolor, footer, emojis_list
from secret1 import bitly_token
import pyshorteners

get_data_timer: list = [30]

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
def moodle_color(i: int, assignmentsdata: dict):
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
def check_command_style(
    dict: dict,
    amount: str = "",
    color: str = "",
    status: int = None,
    done_list: list = None,
):
    # Url shortener
    shorter_url = pyshorteners.Shortener(api_key=bitly_token)

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
            done_list[0] += 1

        elif dict["hwstatus"] == "Tarefa não entregue":
            embed.set_author(
                name=dict["hwstatus"],
                icon_url="https://i1.pngguru.com/preview/326/505/102/red-cross-emoji-discord-logo-line-soviet-union-material-property-symbol-png-clipart.jpg",
            )

        else:
            done_list[1] += 1

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

    embed.add_field(
        name="Link", value=shorter_url.bitly.short(dict["link"]), inline=False
    )

    embed.add_field(name="Professor", value=dict["author"], inline=False)

    embed.set_footer(text=footer)
    return embed, done_list


# Style for group command
def group_command_style(member: list, amount: int) -> Embed:
    embed = Embed(
        title="How to use it: ",
        description="To join this group you must react with the respective emoji",
        color=defaultcolor,
    )

    embed.set_author(name="Group Making Tool")

    embed.add_field(
        name=f"Member {emojis_list[0]}",
        value=f"`{member}`",
        inline=False,
    )

    for people in range(amount - 1):
        embed.add_field(
            name=f"Member {emojis_list[people+1]}",
            value=f"Click on the emoji to join as member {people+1}",
            inline=False,
        )

    embed.set_footer(text=footer)

    return embed
