from typing import Optional

from discord.ext.commands import Cog, command
from discord.utils import get

from settings import allowed_channels
from utilities import help_message, main_messages_style


def syntax(command):
    cmd_and_aliases = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

    params = " ".join(params)

    return f"```{cmd_and_aliases} {params}```"


class Help(Cog):
    def __init__(self, client):
        self.client = client
        self.client.remove_command("help")

    async def cmd_help(self, ctx, command):
        embed = main_messages_style(f"Help with `<{command}>`", syntax(command))
        embed.add_field(name="Command description", value=command.help)
        await ctx.send(embed=embed)

    @command(name="help", aliases=["show_help", "HELP", "Help", "h"])
    async def show_help(self, ctx, cmd: Optional[str]):
        if str(ctx.channel.id) in allowed_channels:
            if not cmd:
                contents = [
                    [
                        "Moodle",
                        [
                            "get",
                            "Get all events, assignments or classes informations from Moodle",
                        ],
                        [
                            "check",
                            "Receive privately more information about assignments",
                        ],
                        [
                            "getToken",
                            "Create or get your MoodleAPI Token decrypted. The token is used to check your assignments status on Moodle",
                        ],
                    ],
                    [
                        "General",
                        [
                            "clear",
                            "Delete chat messages for the typed amount (Only if you have permission to manage messages on that chat)",
                        ],
                        ["help", "All commands information"],
                        [
                            "profile",
                            "Profile command is used to show someones profile, levels and experience, you can mention another member to see his profile or leave it in blank to see your own",
                        ],
                        [
                            "chat_permission",
                            "Allow, revoke or shows you the text channels in which the bot can read commands/work on",
                        ],
                        [
                            "reminder",
                            "Creates a personal reminder about a moodle event or about anything you want to",
                        ],
                        [
                            "ping",
                            "Shows the bot latency (This command does not requires the server preposition)",
                        ],
                        ["printm", "Prints an embed message on the text channel"],
                    ],
                    [
                        "Fun/Games",
                        ["cipher", "Encrypt an message with Caesar Cipher"],
                        ["roll", "Roll a dice"],
                        [
                            "avatar",
                            "Command to show someones avatar on the chat, you must mention the user or leave it in blank to see your own avatar",
                        ],
                        ["e&o", "This command will pick randomly between ever or odd"],
                    ],
                    [
                        "Music",
                        ["join", "Makes the bot join your voice channel"],
                        ["leave", "Makes the bot leave the voice channel"],
                    ],
                    [
                        "Admin",
                        [
                            "createRoles",
                            "Creates a reaction role menu, you must use the respective roles name and emojis",
                        ],
                    ],
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