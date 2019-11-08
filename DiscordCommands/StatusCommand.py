import discord
import os
from discord.ext import commands


def run(Bot, config, GUILD, CHANNEL_ID):

    @Bot.command(name='status')
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                CMD_PATH = config['SCRIPT']['Path']
                CMD = "test.cmd"
                if os.path.exists(CMD_PATH + CMD):
                    await ctx.send("Running " + CMD +  " ...")

                    try:
                        msg = os.popen(CMD_PATH + CMD).read()
                    except OSError as e:
                        msg = "Error: " + e
                    except:
                        msg = "Unkown error occurred!"
                    await ctx.send("```" + msg + "```")
                else:        
                    await ctx.send("Error! " + CMD_PATH + CMD + " don't exist")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
