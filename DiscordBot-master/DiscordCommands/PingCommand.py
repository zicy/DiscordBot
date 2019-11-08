import discord
from discord.ext import commands


def run(Bot, GUILD, CHANNEL_ID):

    #Bot = self.bot

    @Bot.command(name="ping")
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                await ctx.send("Pong")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
    
