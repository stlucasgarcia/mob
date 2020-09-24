from typing import Optional

from discord.ext.commands import Cog, command
from discord.ext.menus import MenuPages, ListPageSource
from discord.utils import get

from bot.utilities import main_messages_style


def syntax(command):
    cmd_and_aliases = '|'.join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ('self', 'ctx'):
            params.append(f'[{key}]' if 'NoneType' in str(value) else f'<{key}>')

    params = ' '.join(params)

    return f'```{cmd_and_aliases} {params}```'


class HelpMenu(ListPageSource):

    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=6)

    async def write_page(self, menu, fields=[]):
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = main_messages_style('Help',
                                    'Welcome to Mack help!',
                                    fot=f'{offset:,} - {min(len_data, offset+self.per_page-1):,}'
                                        f' of {len_data:,} commands.' + ' '*140,
                                    thumb=True)

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append((entry.brief or "No description", syntax(entry)))

        return await self.write_page(menu, fields)


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
            menu = MenuPages(source=HelpMenu(ctx, list(self.client.commands)),
                             delete_message_after=True,
                             timeout=60.0)

            await menu.start(ctx)

        else:
            if command := get(self.client.commands, name=cmd):
                await self.cmd_help(ctx, command)

            else:
                await ctx.send("Command does not exist.")


def setup(client):
    client.add_cog(Help(client))