import discord
from discord.ext import commands


def run(Bot):

    #Bot = self.bot

    @Bot.command(name="selfstop")
    async def _cmd(ctx):
        await ctx.send("Stopping . . .")
        await ctx.bot.close()



    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
