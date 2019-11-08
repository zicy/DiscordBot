import discord
import os
from discord.ext import commands


def run(Bot, GUILD, CHANNEL_ID):

    #Bot = self.bot

    @Bot.command(name='status')
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                cmd = "Status.sh"
                if os.path.exists(cmd):
                    await ctx.send("Running " + cmd +  " ...")
                else:        
                    await ctx.send("Error! " + cmd + " don't exist")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
