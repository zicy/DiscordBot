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
from datetime import datetime
### Status Script


def run(Bot, logging, config, GUILD, CHANNEL_ID):

    @Bot.command(name='status')
    async def _cmd(ctx, *args):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                 logging.info("Command !status used by - " + ctx.message.author)

                select_query = ""
                for var in args:
                    select_query = select_query + "'" + var + "', "
                    if var.lower() in ['a', 'all', 'alle']:
                       select_query = ""
                       break

                if select_query != "":
                    select_query = select_query[:-2]
                    select_query = "AND name IN (" + select_query + ")"
                else:
                    logging.info("Ussage: !status <server> \nExample: !server novus")
                    await ctx.send("Ussage: !status <server> \nExample: !server novus")
                    return

                try:
                    conn = mysql.connector.connect(
                      host=config['DATABASE']['Host'],
                      user=config['DATABASE']['User'],
                      passwd=config['DATABASE']['Password'],
                      database=config['DATABASE']['Database']
                    )

                    mycursor = conn.cursor()
                    mycursor.execute("SELECT id,name,ip,game_port FROM mcp_server WHERE game_port != '0' " + select_query)
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
                            server = MinecraftServer.lookup("{0}:{1}".format(ip, game_port))
                            status = server.status()

                            latency=format(status.latency)
                            players_online=format(status.players.online)
                            players_max=format(status.players.max)
                            version=format(status.version.name)
                            description=status.description

                        except OSError as err:
                            embed=discord.Embed(title=name, description="Offline", color=0xcc0000)
                            embed.set_footer(text=datetime.now(tz=None))
                            await ctx.send(embed=embed)
                            logging.warning("Server '" + name + "' ONLINE")
                        except AttributeError:
                            logging.exception(traceback.print_exc())
                        except:
                            await ctx.send("Unexpected error:", sys.exc_info()[0])
                            logging.exception("Unexpected error:", sys.exc_info()[0])

                        embed=discord.Embed(title=name, description="Online", color=0x185e0d)
                        embed.add_field(name="Players ", value=players_online + "/" + players_max, inline=True)
                        embed.add_field(name="Latency", value=latency, inline=True)
                        embed.add_field(name="Version", value=version, inline=False)
                        embed.set_footer(text=datetime.now(tz=None))
                        await ctx.send(embed=embed)
                        logging.info("Server '" + name + "' ONLINE")

                except Error as e:
                    await ctx.send(":thumbsdown: Error reading data from MySQL table \n" + e)
                    logging.exception("Error reading data from MySQL table \n" + e)
                finally:
                    if (conn.is_connected()):
                        conn.close()
                        mycursor.close()
                        logging.debug("MySQL connection closed")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")