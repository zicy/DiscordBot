import discord
from discord.ext import commands


def run(Bot, logging, GUILD, CHANNEL_ID):

    @Bot.command(name="ping")
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                logging.info("Command !ping used by - " + str(ctx.message.author))

                logging.info("Pong!")
                await ctx.send("Response: Pong!")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            logging.error("Unknown error!")
            await ctx.send("Unknown error!")
    
