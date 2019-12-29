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

class MyCog(commands.Cog):
    def __init__(self, bot, config, GUILD, CHANNEL_ID):
        self.index = 0
        self.bot = bot
        self.config = config
        self.guild = GUILD
        self.channel_id = CHANNEL_ID
        self.channel = self.bot.get_channel(self.channel_id)
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=10.0)
    async def printer(self):
        print(self.index)
        self.index += 1

        try:
            conn = mysql.connector.connect(
                host=self.config['DATABASE']['Host'],
                user=self.config['DATABASE']['User'],
                passwd=self.config['DATABASE']['Password'],
                database=self.config['DATABASE']['Database']
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
                    print("Server: " + name + " OFFLINE")
                    embed=discord.Embed(title=name, description="Offline", color=0xcc0000)
                    embed.set_footer(text=datetime.now(tz=None))
                    await self.channel.send(embed=embed)
                except AttributeError:
                    traceback.print_exc()
                except:
                    await ctx.send("Unexpected error:", sys.exc_info()[0])
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

    @printer.before_loop
    async def before_printer(self):
        print('waiting...')
        await self.bot.wait_until_ready()