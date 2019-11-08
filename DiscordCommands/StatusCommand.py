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
                if os.path.exists(CMD_PATH):
                    await ctx.send("Running " + CMD +  " ...")
                    msg = os.popen(CMD_PATH, CMD).read()
                    await ctx.send("```" + msg + "```")
                else:        
                    await ctx.send("Error! " + CMD_PATH + " don't exist")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
