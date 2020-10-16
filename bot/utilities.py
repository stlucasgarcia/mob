from discord import Embed
from itertools import cycle


# Emojis lists to be used in the entire project 
positive_emojis_list = cycle(["👍", "🆗", "🤙", "👌", "👊", "🆒", "✅"]) 
negative_emojis_list = cycle(["🚫", "🛑", "❌", "⛔"])
status_list = cycle(["Estudando...", "Navegando no Moodle", "Descobrindo tarefas", "Dominando o mundo", "Reduzindo as suas faltas", "Calculando as suas médias"])
books_list = cycle(["📚", "📔", "📕", "📖", "📗", "📘", "📙", "📑", "🧾", "📅", "📆", "🗓"])
happy_faces = cycle(["😀", "😁", "😃", "😄", "😅", "😉", "😊", "😋", "😎", "🙂", "🤗", "😛"])


footer = "Created with 💖 by Mackenzie Students."
thumbnail_url = "https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo-3.png"
url = 'https://eadmoodle.mackenzie.br/'
trans = '\n<:name:758840767786516520>'
defaultcolor = 0x9f000c


# This file is created to style the bot messages
# Styling the check command from moodle.py
def check_command_style(dict, amount="", color="", status=None, done=None):
    embed=Embed(title=dict["modulename"] + " - " + amount, color= color if color else defaultcolor)
    embed.set_thumbnail(url=thumbnail_url)
    embed.add_field(name="Matéria", value=dict["fullname"], inline=True)
    embed.add_field(name="Nome da tarefa", value=dict["name"], inline=True)

    if status == 1:
        if dict["hwstatus"] == "Tarefa entregue":
            embed.set_author(name=dict["hwstatus"] + " " + dict["hwstatus_time"],icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Checkmark_green.svg/1200px-Checkmark_green.svg.png")
            done += 1
        else:
            embed.set_author(name=dict["hwstatus"],icon_url="https://i1.pngguru.com/preview/326/505/102/red-cross-emoji-discord-logo-line-soviet-union-material-property-symbol-png-clipart.jpg")


    if dict["description"] != "Descrição não disponível":
        embed.add_field(name="Descrição", value=dict["description"], inline=False)
        embed.add_field(name="Tipo de tarefa", value=dict["modulename"], inline=True)
    else:
        embed.add_field(name="Tipo de tarefa", value=dict["modulename"], inline=False)


    if dict["modulename"] == "Aula ao vivo - BigBlueButton":
        embed.add_field(name="Data da aula", value=dict["deadline"], inline=True)
    else:
        embed.add_field(name="Data de entrega", value=dict["deadline"], inline=True)


    embed.add_field(name="Link", value=dict["link"], inline=False)
    embed.add_field(name="Professor", value=dict["author"], inline=False)
    embed.set_footer(text=footer)
    return embed, done


# Creating a template for messages
def main_messages_style(name="", message="", emote="", color="", fot="", thumb=False):
    message = f"**{message}**" if message != "" else message
    embed=Embed(title=name, description=f"{message} {emote if emote != '' else emote}",
    color= color if color else defaultcolor)

    if thumb:
        embed.set_thumbnail(url=thumbnail_url)

    embed.set_author(name="")
    embed.set_footer(text=fot + footer)
    return embed


# Template message for help
def help_message(contents):
    embed = Embed(title='Standard Commands',
                  description='Type `mack help [command]` for more help eg. `mack help get`',
                  color=defaultcolor)
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text=footer)

    for row in range(len(contents)):
        name, value = contents[row][0], ''

        for elem in contents[row][1:]:
            value += f'[`{elem[0]}`{trans if row == 0 and contents[row].index(elem) == 3 else ""}]({url} "{elem[1]}")  '

        embed.add_field(name=name, value=value, inline=True)
            
    return embed


FULL_MONTHS = {'janeiro': 1,  'fevereiro': 2, u'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}


def formatTime(seconds):
    hours = seconds // 3600

    seconds %= 3600

    minutes = seconds // 60

    seconds %= 60

    if hours == 0:
        return "%02i:%02i" % (minutes, seconds)
    else:
        return "%02i:%02i:%02i" % (hours, minutes, seconds)