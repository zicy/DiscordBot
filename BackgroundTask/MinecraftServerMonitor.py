### Status Script
import json
import mysql.connector
import socket
import sys
import traceback
### Status Script

import discord
import asyncio
from discord.ext import tasks, commands
### Status Script
from mcstatus import MinecraftServer
from mysql.connector import Error
from datetime import datetime
### Status Script


async def Background_Monitor_Task(self, logging, config, CHANNEL_ID):
    await self.wait_until_ready()
    channel = self.get_channel(CHANNEL_ID)

    while not self.is_closed():

        try:
            conn = mysql.connector.connect(
                host=config['DATABASE']['Host'],
                user=config['DATABASE']['User'],
                passwd=config['DATABASE']['Password'],
                database=config['DATABASE']['Database']
            )

            mycursor = conn.cursor()
            mycursor.execute("SELECT id,name,ip,game_port FROM mcp_server WHERE monitor != '0'")
            myresult = mycursor.fetchall()

            for data in myresult:
                id=data[0]
                name=data[1]
                ip=data[2]
                game_port=data[3]

                # Default values
                latency=-1
                players_online=0
                players_max=0
                version="Unknown"

                try:
                    logging.info("Testing online state of {0} {1}:{2}".format(name, ip, game_port))
                    server = MinecraftServer.lookup("{0}:{1}".format(ip, game_port))
                    status = server.status()

                    latency=format(status.latency)
                    players_online=format(status.players.online)
                    players_max=format(status.players.max)
                    version=format(status.version.name)
                    description=status.description

                except OSError as err:
                    logging.warning("Server: '{0}' OFFLINE".format(name))
                    embed=discord.Embed(title=name, description="Offline", color=0xcc0000)
                    embed.set_footer(text=datetime.now(tz=None))
                    await channel.send(embed=embed)
                except AttributeError:
                    logging.exception(traceback.print_exc())
                except:
                    await channel.send("Unexpected error:", sys.exc_info()[0])
                    logging.exception("Unexpected error:", sys.exc_info()[0])


        except Error as e:
            await channel.send("Error reading data from MySQL table \n" + e)
            logging.debug("Error reading data from MySQL table \n" + e)
        finally:
            if (conn.is_connected()):
                conn.close()
                mycursor.close()
                logging.debug("MySQL connection closed")

        await asyncio.sleep(int(config['MONITOR']['Interval'])) # task runs every xx seconds