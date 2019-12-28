### Status Script
import json
import mysql.connector
import socket
import sys
import traceback
### Status Script

import discord
import os
import asyncio
from discord.ext import commands
### Status Script
from mcstatus import MinecraftServer
from mysql.connector import Error
### Status Script


def run(Bot, config, GUILD, CHANNEL_ID):

    @Bot.command(name='status')
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):

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
                        #print("Id = ", data[0])
                        #print("Name  = ", data[1])
                        #print("IP = ", data[2])
                        #print("Game Port = ", data[3])

                        id=data[0]
                        name=data[1]
                        ip=data[2]
                        game_port=data[3]
                        print("\n")

                        # Default values
                        online=0
                        latency=-1
                        players_online=0
                        players_max=0
                        version="Unknown"


                        print("Server List Ping")
                        try:
                            server = MinecraftServer.lookup("{0}:{1}".format(ip, game_port))
                            # 'status' is supported by all Minecraft servers that are version 1.7 or higher.
                            status = server.status()
                            #print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))

                            print(" Ping successful")
                            online=1
                            latency=format(status.latency)
                            players_online=format(status.players.online)
                            players_max=format(status.players.max)
                            version=format(status.version.name)
                            description=status.description

                        except OSError as err:
                            #print("Ping failed")
                            #print("  OS error: {0}".format(err))
                            await ctx.send(":thumbsdown: " + name + " did not answer ping...")
                        except AttributeError:
                            traceback.print_exc()
                        except:
                            print(" Unexpected error:", sys.exc_info()[0])

                        # Rating
                        await ctx.send(":thumbsup: " + name + " Online \n Players: " + players_online + "/" + players_max + "")

                        #print("Ping result")
                        #print(" Online = ", online)
                        #print(" Latency = {0} ms".format(latency))
                        #print(" Players = ", players_online)
                        #print(" Max players = ", players_max)
                        #print(" Version = ", version)

                        #print("---------------------------------------------------------------------------------------------------------------")
                        #print("\n")

                except Error as e:
                    #print("Error reading data from MySQL table", e)
                    await ctx.send(":thumbsdown: Error reading data from MySQL table \n" + e)
                finally:
                    if (conn.is_connected()):
                        conn.close()
                        mycursor.close()
                        #print("MySQL connection is closed")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
