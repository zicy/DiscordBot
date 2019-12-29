import discord
from discord.ext import commands


def run(Bot, logging, GUILD, CHANNEL_ID):

    #Bot = self.bot

    @Bot.command(name="rcon")
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                logging.info("Command !rcon used by - " + str(ctx.message.author))

                await ctx.send("Pong")
                logging.info("Response: Pong!")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")