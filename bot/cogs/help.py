from typing import Optional

from discord.ext.commands import Cog, command
from discord.utils import get

from utilities import help_message, main_messages_style


def syntax(command):
    cmd_and_aliases = '|'.join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ('self', 'ctx'):
            params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')

    params = ' '.join(params)

    return f'```{cmd_and_aliases} {params}```'


class Help(Cog):

    def __init__(self, client):
        self.client = client
        self.client.remove_command('help')

    async def cmd_help(self, ctx, command):
        embed = main_messages_style(f'Help with `<{command}>`',
                                    syntax(command))
        embed.add_field(name='Command description', value=command.help)
        await ctx.send(embed=embed)

    @command(name='help')
    async def show_help(self, ctx, cmd: Optional[str]):
        if not cmd:
            contents = [
                ['Moodle', ['get', 'Get all events, assignments or classes informations.'],
                           ['check', 'Recive privetly more informations about assignments.'],
                           ['getToken', 'Create or get your MoodleAPI Token decrypted.']],
                ['General', ['clear', 'Clear chat messages.'],
                            ['help', 'All commands informations.']],
                ['Games', ['cipher', 'Encypt an message with Caesar Cipher.'],
                          ['roll', 'Roll a dice.']],
            ]

            embed = help_message(contents)

            await ctx.send(embed=embed)

        else:
            if command := get(self.client.commands, name=cmd):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("Command does not exist.")


def setup(client):
    client.add_cog(Help(client))