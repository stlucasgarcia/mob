import discord, asyncio

from moodleapi.data.export import Export

from discord.ext import tasks
from discord.ext.commands import command, Cog

from utilities import main_messages_style, check_command_style, happy_faces, negative_emojis_list, books_list, \
    positive_emojis_list, FULL_MONTHS
from utilities_moodle import data_dict, moodle_color, loop_channel

from datetime import datetime as dt


class Reminder(Cog):
    def __init__(self, client):
        self.client = client
        self.reminderLoop.start(ctx=None, discord_id=226485287612710913, guild_id=748168924465594419, values=None,
                                sub=None)

    @command(name="reminder", aliases=["Reminder", " REMINDER", "Remind", "REMIND", "RemindMe", "Rememberme"])
    async def reminder(self, ctx):
        """Reminder is responsable to create reminders for Moodle events or other types"""

        def check(ctx, m):
            return m.author == ctx.author

        embed = main_messages_style("Do you want to create a reminder about a Moodle event?",
                                    "Note: You can create a reminder about a Moodle event or about something personal")
        await ctx.author.send(embed=embed)

        valid_options_yes = ["yes", "sim", "s", "y", "moodle", "certamente que sim", "ss po", "ss", "ok",
                             "vai la vai la", "fechou", "bora", "1", "of course", "sure", "sure thing"] + [
                                positive_emojis_list]
        valid_options_no = ["nao", "não", "n", "no", "0", "nem po", "no, sorry", "i'd rather not", "no buddy",
                            "another day my friend", "nem da", "not ok", "i don't think so", "maybe not",
                            "nem malz"] + [negative_emojis_list]

        option = await self.client.wait_for('message')

        if option.content.lower() in valid_options_yes:

            # Check if there's events
            data = await self.client.pg_con.fetch("SELECT * FROM moodle_events WHERE discord_id = $1 AND guild_id = $2",
                                                  169890240708870144, int(ctx.guild.id))

            # Counter for the amount of assignments/events    
            amount = 0

            # TODO: check month, day and response to time and date style

            if data:
                for index in range(len(data)):
                    amount += 1
                    assignmentsdata = data_dict(data[index])

                    # Styling the message to improve user experience
                    color = moodle_color(index, assignmentsdata)

                    embed = check_command_style(assignmentsdata, str(amount), color, None)[0]
                    await asyncio.sleep(0.5)
                    await ctx.author.send(embed=embed)

                embed = main_messages_style(
                    f"There were a total of {amount} events {next(books_list)} {next(happy_faces)} ",
                    "Note: I am only showing events of 14 days ahead")
                await asyncio.sleep(0.5)
                await ctx.author.send(embed=embed)

                embed = main_messages_style("What event number do you want to be reminded about?")
                await ctx.author.send(embed=embed)

                op = await self.client.wait_for('message')
                op = op.content

                try:
                    op = int(op)
                    subject = data[op - 1][6]

                except Exception:
                    embed = main_messages_style(f"Event number {op.content} doesn't exist")
                    await ctx.author.send(embed=embed)

                    while op != int:
                        embed = main_messages_style("What event number do you want to be reminded about?")
                        await ctx.author.send(embed=embed)

                        try:
                            op = await self.client.wait_for('message')
                            op = int(op.content)

                        except Exception:
                            pass

                op = int(op)
                subject = data[op - 1][6]

                d = [i for i in data[op - 1]]
                d[0] = int(ctx.author.id)
                d[1] = int(d[1])

                midnight = f"Note: The assignment deadline is at the first minute minute of the day {d[9]}" if d[
                                                                                                                   10] == "00:00" else ""

                embed = main_messages_style(
                    f"You will be reminded of {subject} in 3 hours, 1 hour and 15 minutes before the deadline if "
                    f"possible",
                    midnight)

                await ctx.author.send(embed=embed)

                Export('bot_reminder').to_db(data=d)

                await ctx.message.add_reaction(next(positive_emojis_list))

            else:
                await ctx.message.add_reaction(next(negative_emojis_list))

                embed = main_messages_style("There weren't any scheduled events 😑😮",
                                            "Note: You can't create a reminder")
                await ctx.author.send(embed=embed)

        elif option.content.lower() in valid_options_no:
            embed = main_messages_style("What do you want to be reminded about?")
            await ctx.author.send(embed=embed)

            title = await self.client.wait_for('message')
            await asyncio.sleep(1)

            embed = main_messages_style("What time?", "Note: Time format must be HH:MM")
            await ctx.author.send(embed=embed)

            time = await self.client.wait_for('message')
            await asyncio.sleep(1)

            embed = main_messages_style("When?", "Note: Date format must be MM/DD")
            await ctx.author.send(embed=embed)

            date = await self.client.wait_for('message')
            await asyncio.sleep(1)

            data = [int(ctx.author.id), int(ctx.guild.id), None, None, None, None, title.content, None, None,
                    date.content, time.content, None, None]

            Export('bot_reminder').to_db(data=data)

            await ctx.message.add_reaction(next(positive_emojis_list))

            embed = main_messages_style(
                f"You will be reminded of {data[6].title()} in 3 hours, 1 hour and 15 minutes before the deadline if "
                f"possible")
            await ctx.author.send(embed=embed)


        else:
            await ctx.message.add_reaction(next(negative_emojis_list))

            embed = main_messages_style("You must type a valid option", "Note: valid options: `Yes` or `No`")
            await ctx.author.send(embed=embed)

    @reminder.after_invoke
    async def reload_reminder(self, ctx):
        data = await self.client.pg_con.fetch(
            "SELECT deadline, deadline_date, subject_name FROM bot_reminder WHERE discord_id=$1 AND guild_id=$2",
            int(ctx.author.id), int(ctx.guild.id))

        dates, times, subs = [], [], []
        for elem in data:
            if len(elem[0]) > 5:
                dates.append((FULL_MONTHS[elem[0].split()[-1]], int(elem[0].split()[-2])))
            elif len(elem[0]) == 5:
                dates.append((int(elem[0].split('/')[0]), int(elem[0].split('/')[1])))

            times.append((int(elem[1][:2]), int(elem[1][3:5])))
            subs.append(elem[2])

        dat = []
        for i in range(len(dates)):
            dat.append(dt(2020, dates[i][0], int(dates[i][1]), times[i][0], times[i][1]))

        da = dt.today()
        mon, d, h, m = da.month, da.day, da.hour, da.minute
        date = dt(2020, mon, d, h, m)

        date_min = min(dat, key=lambda y: abs(y - date))
        values = [date_min.month, date_min.day, date_min.hour, date_min.minute]
        subject = subs[dat.index(date_min)]

        self.reminderLoop.restart(ctx, int(ctx.author.id), int(ctx.guild.id), values, subject)

    @tasks.loop(minutes=1)
    async def reminderLoop(self, ctx, discord_id, guild_id, values, sub):
        now = dt.today()
        time = [now.month, now.day, now.hour, now.minute]
        # print(values, sub)
        # print(time)

        if values:
            if (values[0] == time[0]) and (values[1] == time[1]):
                i, j = time[2] - values[2], time[3] - values[3]
                # print(i, j)

                if i == 3 and j == 0:
                    embed = main_messages_style(f"The dealine of {sub} is in **3 hours**",
                                                "Note: The next reminder will be in an **hour before the deadline**.")
                    await ctx.author.send(embed=embed)

                elif i == 1 and j == 0:
                    embed = main_messages_style(f"The dealine of {sub} is in **an hour**",
                                                "Note: The next reminder will be in **15 minutes before the "
                                                "deadline**.")
                    await ctx.author.send(embed=embed)

                elif i == 0 and j == 15:
                    embed = main_messages_style(f"The dealine of {sub} is in *15 *minutes**",
                                                "Note: **This is the last reminder**.")
                    await ctx.author.send(embed=embed)

                elif i == 0 and j == 0:
                    await self.client.pg_con.fetch(
                        "DELETE FROM bot_reminder WHERE discord_id=$1 AND guild_id=$2 AND subject_name=$3",
                        discord_id, guild_id, sub)


def setup(client):
    client.add_cog(Reminder(client))
