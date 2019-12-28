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
                        print("Id = ", data[0])
                        print("Name  = ", data[1])
                        print("IP = ", data[2])
                        print("Game Port = ", data[3])

                        id=data[0]
                        name=data[1]
                        ip=data[2]
                        game_port=data[3]
                        print("\n")

                        # Default values
                        query_error=0

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
                            print(" Ping failed")
                            print("  OS error: {0}".format(err))
                        except AttributeError:
                            traceback.print_exc()
                        except:
                            print(" Unexpected error:", sys.exc_info()[0])

                        # Rating
                        print("Ping result")
                        print(" Online = ", online)
                        print(" Latency = {0} ms".format(latency))
                        print(" Players = ", players_online)
                        print(" Max players = ", players_max)
                        print(" Version = ", version)

                        print("---------------------------------------------------------------------------------------------------------------")
                        print("\n")

                except Error as e:
                    print("Error reading data from MySQL table", e)
                finally:
                    if (conn.is_connected()):
                        conn.close()
                        mycursor.close()
                        print("MySQL connection is closed")

                #CMD_PATH = config['SCRIPT']['Path']
                #CMD = "test.cmd"
                #if os.path.exists(CMD_PATH + CMD):
                #    await ctx.send("Running " + CMD +  " ...")

                #    proc = await asyncio.create_subprocess_shell(CMD_PATH + CMD, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                #    out, err = await proc.communicate()

                #    if out:
                #        await ctx.send("```\n[" + CMD + "]\n" + out.decode() + "\n```")
                #    if err:
                #        await ctx.send("```\n[" + CMD + "]\n" + err.decode() + "\n```")

                #else:        
                #    await ctx.send("Error! " + CMD_PATH + CMD + " don't exist")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
