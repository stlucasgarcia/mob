import discord
darkred = 0x9f000c

# def assignments_style(modulename, fullname, name, description, deadline, link):


def assignments_style(dict):
    embed=discord.Embed(title=dict["modulename"], color=darkred)
    embed.set_thumbnail(url="https://logodownload.org/wp-content/uploads/2017/09/mackenzie-logo-3.png")
    embed.add_field(name="Matéria", value=dict["fullname"], inline=True)
    embed.add_field(name="Nome da tarefa", value=dict["name"], inline=True)
    embed.add_field(name="Descrição", value=dict["description"], inline=False)
    embed.add_field(name="Tipo de tarefa", value=dict["modulename"], inline=True)
    embed.add_field(name="Data de entrega", value=dict["deadline"], inline=True)
    embed.add_field(name="Link", value=dict["link"], inline=False)
    embed.set_footer(text="Feito com 💖 por alunos do Mackenzie.")
    return embed


def main_messages_style(message, emote="", color=""):
    
    embed=discord.Embed(description=f"**{message}** {emote if emote != '' else emote}", color= color if color else darkred)
    embed.set_footer(text="Feito com 💖 por alunos do Mackenzie.")
    return embed
