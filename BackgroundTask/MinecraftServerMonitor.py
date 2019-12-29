### Status Script
import json
import mysql.connector
import socket
import sys
import traceback
### Status Script

import discord
from discord.ext import tasks, commands
### Status Script
from mcstatus import MinecraftServer
from mysql.connector import Error
from datetime import datetime
### Status Script


async def Background_Monitor_Tast(self, config, CHANNEL_ID):
    await self.wait_until_ready()
    counter = 0
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
            mycursor.execute("SELECT id,name,ip,game_port FROM mcp_server WHERE game_port != '0'")
            myresult = mycursor.fetchall()

            for data in myresult:
                id=data[0]
                name=data[1]
                ip=data[2]
                game_port=data[3]

                # Default values  await self.channel.send("Ussage: !status <server> \nExample: !server novus")
                latency=-1
                players_online=0
                players_max=0
                version="Unknown"

                try:
                    server = MinecraftServer.lookup("{0}:{1}".format(ip, game_port))
                    status = server.status()

                    latency=format(status.latency)
                    players_online=format(status.players.online)
                    players_max=format(status.players.max)
                    version=format(status.version.name)
                    description=status.description

                except OSError as err:
                    print("Server: '" + name + "' OFFLINE")
                    #embed=discord.Embed(title=name, description="Offline", color=0xcc0000)
                    #embed.set_footer(text=datetime.now(tz=None))
                    #await channel.send(embed=embed)
                except AttributeError:
                    traceback.print_exc()
                except:
                    #await ctx.send("Unexpected error:", sys.exc_info()[0])
                    print("Unexpected error:", sys.exc_info()[0])

                #embed=discord.Embed(title=name, description="Online", color=0x185e0d)
                #embed.add_field(name="Players ", value=players_online + "/" + players_max, inline=True)
                #embed.add_field(name="Latency", value=latency, inline=True)
                #embed.add_field(name="Version", value=version, inline=False)
                #embed.set_footer(text=datetime.now(tz=None))
                #await ctx.send(embed=embed)

        except Error as e:
            #await ctx.send(":thumbsdown: Error reading data from MySQL table \n" + e)
            print("Error reading data from MySQL table \n" + e)
        finally:
            if (conn.is_connected()):
                conn.close()
                mycursor.close()


        counter += 1
        await channel.send(counter)
        await asyncio.sleep(60) # task runs every 60 seconds