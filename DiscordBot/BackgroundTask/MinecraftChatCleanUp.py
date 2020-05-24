### Status Script
import socket
import sys
### Status Script

import discord
import asyncio
from discord.ext import tasks, commands

### Status Script
from datetime import datetime, timedelta, timezone
### Status Script


async def Background_Monitor_Task(self, logging, config, CHANNEL_ID):
    await self.wait_until_ready()
    channel = self.get_channel(int(config['MC_CHAT_CLEANUP']['Channel_ID']))
    admin_notification_channel = self.get_channel(int(config['BOT']['AdminNotificationChannel']))
    time_to_delete = int(config['MC_CHAT_CLEANUP']['CleanupTime'])


    while not self.is_closed():

        ### Delete messages
        try:
            date = datetime.utcnow() - timedelta(minutes=time_to_delete)

            deleted = await channel.purge(limit=200, before=date)

            if len(deleted) != 0:
                delete_success = True
            else:
                delete_success = False
        except discord.Forbidden as e:
            delete_success = False

            try:
                await admin_notification_channel.send("Permission error in channel '{}' message '{}'".format(channel.name, e), delete_after=10)

            except discord.Forbidden as e:
                logging.error("Permission error in channel '{}' message '{}'".format(admin_notification_channel.name, e))

            except:
                logging.error("Unexpected error:", sys.exc_info()[0])

        except:
            delete_success = False
            logging.error("Unexpected error:", sys.exc_info()[0])

        ### Report number of delete messages
        try:
            if delete_success:

                delete_self_after = 120
                current_time = datetime.utcnow()

                embed=discord.Embed(title="Minecraft Chat cleanup", color=0x0696bf, timestamp=current_time)
                embed.add_field(name="Deleted messages older than {} minute(s)".format(time_to_delete), value=len(deleted), inline=True)
                embed.add_field(name="Auto deleted this message after", value="{} sec".format(delete_self_after), inline=True)
                embed.set_footer(text=self.user)

                await admin_notification_channel.send(embed=embed, delete_after=delete_self_after)

        except discord.Forbidden as e:
            logging.error("Permission error in channel '{}' message '{}'".format(channel, e))

        except:
            logging.error("Unexpected error:", sys.exc_info()[0])


        await asyncio.sleep(int(config['MC_CHAT_CLEANUP']['Interval'])) # task runs every xx seconds