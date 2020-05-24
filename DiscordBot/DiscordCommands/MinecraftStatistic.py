import discord
import asyncio
import sys
import traceback
import os
import mysql.connector
from discord.ext import commands
from mysql.connector import Error
from datetime import datetime


def run(Bot, logging, config):

    @Bot.command(
        name = 'statistic',
        aliases = ['stats', 'stat'],
        help = 'Giver Minecraft statestik om en spiller',
        usage = 'navn',
        description = 'Statestik for Minecraft spiller på Crafters.dk')
    @commands.has_permissions(administrator=True)
    async def _cmd(ctx, player):
        logging.info("Command !stats used by - " + str(ctx.message.author))

        # Default values
        blocks_mined = 0
        blocks_placed = 0
        command_lines = 0
        chat_lines = 0
        pvp_kills = 0
        pve_kills = 0
        playtime_sec = 0
        playtime = ""
        stats_found = False

        # Stats (mined, placed etc
        try:
            conn = mysql.connector.connect(
                host=config['DATABASE']['Host'],
                user=config['DATABASE']['User'],
                passwd=config['DATABASE']['Password'],
                database=config['DATABASE']['Database']
            )

            mycursor = conn.cursor(prepared=True)
            sql = "SELECT uuid, type, SUM(count) AS count FROM mcp_stats_lb WHERE last_name = %s GROUP BY type"
            mycursor.execute(sql, (player,))
            myresult = mycursor.fetchall()
            
            num_rows = mycursor.rowcount

            if num_rows != 0:
                for data in myresult:
                    uuid = data[0].decode()
                    type = data[1]
                
                    if type == 0: # mined
                        blocks_mined = '{:,}'.format(int(data[2].decode())).replace(',', '.')
                    elif type == 1:
                        blocks_placed = '{:,}'.format(int(data[2].decode())).replace(',', '.')
                    elif type == 2:
                        command_lines = '{:,}'.format(int(data[2].decode())).replace(',', '.')
                    elif type == 3:
                        chat_lines = '{:,}'.format(int(data[2].decode())).replace(',', '.')
                    elif type == 4:
                        pvp_kills = '{:,}'.format(int(data[2].decode())).replace(',', '.')
                    elif type == 5:
                        pve_kills = '{:,}'.format(int(data[2].decode())).replace(',', '.')

                    stats_found = True
            else:
                stats_found = False

        except Error as e:
            await ctx.send(":thumbsdown: Error reading data from MySQL table \n" + e)
            logging.exception("Error reading data from MySQL table \n" + e)
        except:
            await ctx.send("Unexpected error:", sys.exc_info()[0])
            logging.exception("Unexpected error:", sys.exc_info()[0])
        finally:
            if (conn.is_connected()):
                conn.close()
                mycursor.close()
                logging.info("MySQL connection closed")

        # Stats playtime
        try:
            conn = mysql.connector.connect(
                host=config['DATABASE']['Host'],
                user=config['DATABASE']['User'],
                passwd=config['DATABASE']['Password'],
                database=config['DATABASE']['Database']
            )

            mycursor = conn.cursor(prepared=True)
            sql = "SELECT type, SUM(count) AS count FROM mcp_stats_lb_players WHERE type = 2 AND server = 0 AND uuid = %s"
            mycursor.execute(sql, (uuid,))
            myresult = mycursor.fetchall()
            
            num_rows = mycursor.rowcount


            if num_rows != 0:
                for data in myresult:
                    type = data[0]
                
                    if type == 2: # playtime
                        playtime_sec = int(data[1].decode())

                    stats_found = True
            else:
                stats_found = False

        except Error as e:
            await ctx.send(":thumbsdown: Error reading data from MySQL table \n" + e)
            logging.exception("Error reading data from MySQL table \n" + e)
        except:
            await ctx.send("Unexpected error:", sys.exc_info()[0])
            logging.exception("Unexpected error:", sys.exc_info()[0])
        finally:
            if (conn.is_connected()):
                conn.close()
                mycursor.close()
                logging.info("MySQL connection closed")

        # 
        delete_msg_after = 120 # time in sec
        current_time = datetime.utcnow()


        def display_time(seconds, granularity=2):
            result = []

            intervals = (
                ('dage', 86400),    # 60 * 60 * 24
                ('timer', 3600),    # 60 * 60
                ('minutter', 60),
                ('sekunder', 1),
                )

            for name, count in intervals:
                value = seconds // count
                if value:
                    seconds -= value * count
                    if value == 1:
                        name = name.rstrip('s')
                    result.append("{} {}".format(value, name))
            return ', '.join(result[:granularity])


        if stats_found:
            embed=discord.Embed(title="Statistik for {}".format(player), description="blah blah blah ...", color=0x185e0d, timestamp=current_time, url="https://crafters.dk/statistik/")
            embed.add_field(name="Blokke placeret", value=blocks_placed, inline=True)
            embed.add_field(name="Blokke minet", value=blocks_mined, inline=True)
            embed.add_field(name="Chat linjer", value=chat_lines, inline=True)
            embed.add_field(name="Kommandoer", value=command_lines, inline=True)
            embed.add_field(name="PvP kills", value=pvp_kills, inline=True)
            embed.add_field(name="PvE kills", value=pve_kills, inline=True)
            embed.add_field(name="Spilletid", value=display_time(playtime_sec, 4), inline=False)
            embed.set_thumbnail(url="https://crafatar.com/renders/body/{}?helm&scale=8&default=alex".format(uuid))
            embed.set_footer(text="Se mere på https://crafters.dk/statistik/")
            await ctx.send(embed=embed, delete_after=delete_msg_after)
            await ctx.message.delete(delay=delete_msg_after)
        else:
            embed=discord.Embed(title="Statistik for {}".format(player), description="Fandt ikke noget for spilleren {}".format(player), color=0xcc0000, timestamp=current_time, url="https://crafters.dk/statistik/")
            embed.set_footer(text=datetime.now(tz=None))
            await ctx.send(embed=embed, delete_after=delete_msg_after)
            await ctx.message.delete(delay=delete_msg_after)

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")