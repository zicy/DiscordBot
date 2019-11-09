import discord
import os
import asyncio
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

                    proc = await asyncio.create_subprocess_shell(CMD_PATH + CMD, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
                    out, err = await proc.communicate()

                    if out:
                        await ctx.send("```\n [" + CMD + "]\n" + out.decode() + " \n```")
                    if err:
                        await ctx.send("```\n [" + CMD + "]\n" + err.decode() + " \n```")

                else:        
                    await ctx.send("Error! " + CMD_PATH + CMD + " don't exist")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
