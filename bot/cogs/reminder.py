import discord, asyncio

from moodleapi.data.export import Export

from discord.ext.commands import command, Cog

from utilities import main_messages_style, check_command_style, happy_faces, negative_emojis_list, books_list, positive_emojis_list 
from utilities_moodle import data_dict, moodle_color, loop_channel


class Reminder(Cog):
    def __init__(self, client):
        self.client = client

    @command(name="reminder", aliases=["Reminder", " REMINDER", "Remind", "REMIND", "RemindMe", "Rememberme"])
    async def reminder(self, ctx):
        """Reminder is responsable to create reminders for Moodle events or other types"""

        def check(ctx, m):
            return m.author == ctx.author
        
        embed =  main_messages_style("Do you want to create a reminder about a Moodle event?", "Note: You can create a reminder about a Moodle event or about something personal")
        await ctx.author.send(embed=embed)
        
        valid_options_yes = ["yes", "sim", "s", "y", "moodle", "certamente que sim", "ss po", "ss", "ok", "vai la vai la", "fechou", "bora", "1", "of course", "sure", "sure thing"] + [positive_emojis_list]
        valid_options_no = ["nao", "não", "n", "no", "0", "nem po", "no, sorry", "i'd rather not", "no buddy", "another day my friend",  "nem da", "not ok", "i don't think so", "maybe not"] + [negative_emojis_list]
        
        option = await self.client.wait_for('message')

        if option.content.lower() in valid_options_yes:

            # Check if there's events
            data = await self.client.pg_con.fetch("SELECT * FROM moodle_events WHERE discord_id = $1 AND guild_id = $2", 169890240708870144, int(ctx.guild.id))
            
            # Counter for the amount of assignments/events    
            amount = 0

            if data:
                for index in range(len(data)):
                    amount += 1
                    assignmentsdata = data_dict(data[index])

                    #Styling the message to improve user experience
                    color = moodle_color(index, assignmentsdata)

                    embed = check_command_style(assignmentsdata, str(amount), color, None)[0]
                    await asyncio.sleep(0.5)
                    await ctx.author.send(embed=embed)

                embed = main_messages_style(f"There were a total of {amount} events {next(books_list)} {next(happy_faces)} ", "Note: I am only showing events of 14 days ahead")
                await asyncio.sleep(0.5)
                await ctx.author.send(embed=embed)

                embed = main_messages_style("What event number do you want to be reminded about?")
                await ctx.author.send(embed=embed)
                
                op = await self.client.wait_for('message')
                op = op.content

                try:
                    op = int(op)
                    subject = data[op-1][6]

                except Exception:
                    embed =  main_messages_style(f"Event number {op.content} doesn't exist")
                    await ctx.author.send(embed=embed)

                    while op != int:
                        embed =  main_messages_style("What event number do you want to be reminded about?")
                        await ctx.author.send(embed=embed)

                        try:
                            op = await self.client.wait_for('message')
                            op = int(op.content)
                        
                        except Exception:
                            pass
                

                op = int(op)
                subject = data[op-1][6]
                
                d = [i for i in data[op-1]]
                d[0] = int(ctx.author.id)
                d[1] = int(d[1])

                midnight = f"Note: The assignment deadline is at the first minute minute of the day {d[9]}" if d[10] == "00:00" else ""
                
                embed = main_messages_style(f"You will be reminded of {subject} in 3 hours, 1 hour and 15 minutes before the deadline if possible", midnight)

                await ctx.author.send(embed=embed)

                Export('bot_reminder').to_db(data=d)

                await ctx.message.add_reaction(next(positive_emojis_list))

            else:
                await ctx.message.add_reaction(next(negative_emojis_list))

                embed = main_messages_style("There weren't any scheduled events 😑😮", "Note: You can't create a reminder")
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


            data = [int(ctx.author.id), int(ctx.guild.id), None, None, None, None, title.content, None, None, date.content, time.content, None, None]
            
            Export('bot_reminder').to_db(data=data)

            await ctx.message.add_reaction(next(positive_emojis_list))

            embed = main_messages_style(f"You will be reminded of {data[6].title()} in 3 hours, 1 hour and 15 minutes before the deadline if possible")
            await ctx.author.send(embed=embed)


        else:
            await ctx.message.add_reaction(next(negative_emojis_list))

            embed = main_messages_style("You must type a valid option", "Note: valid options: `Yes` or `No`")
            await ctx.author.send(embed=embed)



def setup(client):
    client.add_cog(Reminder(client))