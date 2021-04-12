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


def convert_to_seconds(s):
    seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
    return int(s[:-1]) * seconds_per_unit[s[-1]]


async def Background_Monitor_Task(self, logging, config, CHANNEL_ID):
    await self.wait_until_ready()

    #channel = self.get_channel(int(config['MC_CHAT_CLEANUP']['Channel_ID']))
    #admin_notification_channel = self.get_channel(int(config['BOT']['AdminNotificationChannel']))
    #time_to_delete = int(config['MC_CHAT_CLEANUP']['CleanupTime'])




    while not self.is_closed():

        sections = list(filter(lambda x:'-OPTIONS' in x, config.sections()))
        for guild_options in sections: 
            channels_clean = config[guild_options]['Purge_Chats']
            notification_channel = self.get_channel(int(config[guild_options]['Admin_Notification_Channel']))
            channels = channels_clean.split(',')

            for channel_options in channels:
                options = channel_options.split(".")
                channel = options[0]
                time_delete = options[1]
                time_to_delete = convert_to_seconds(time_delete)
    
                print("Guild: " + guild_options + " Channel: " + channel + " Delete older than: " + str(time_to_delete))

                channel = self.get_channel(int(channel))
                time_to_delete = time_to_delete
                
                ### Delete messages
                try:
                    date = datetime.utcnow() - timedelta(seconds=time_to_delete)

                    deleted = await channel.purge(limit=200, before=date, check=lambda msg: not msg.pinned)

                    if len(deleted) != 0:
                        delete_success = True
                    else:
                        delete_success = False
                except discord.Forbidden as e:
                    delete_success = False

                    try:
                        await notification_channel.send("Permission error in channel '{}' message '{}'".format(channel.name, e), delete_after=10)

                    except discord.Forbidden as e:
                        logging.error("Permission error in channel '{}' message '{}'".format(notification_channel.name, e))

                    except:
                        logging.error("Unexpected error:", sys.exc_info()[0])

                except:
                    delete_success = False
                    logging.error("Unexpected error:", str(sys.exc_info()[0]))

                ### Report number of delete messages
                try:
                    if delete_success:

                        delete_self_after = 300
                        current_time = datetime.utcnow()

                        embed=discord.Embed(title="Cleaned up messages in '{}'".format(channel.name), color=0x0696bf, timestamp=current_time)
                        embed.add_field(name="Deleted messages older than {}".format(time_delete), value=len(deleted), inline=True)
                        embed.set_footer(text=self.user)

                        await notification_channel.send(embed=embed, delete_after=delete_self_after)

                except discord.Forbidden as e:
                    logging.error("Permission error in channel '{}' message '{}'".format(channel, e))

                except:
                    logging.error("Unexpected error:", sys.exc_info()[0])


        await asyncio.sleep(int(config['MC_CHAT_CLEANUP']['Interval'])) # task runs every xx seconds
