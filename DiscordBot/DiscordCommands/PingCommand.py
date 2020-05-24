import discord
from discord.ext import commands


def run(Bot, logging, GUILD, CHANNEL_ID):

    @Bot.command(name="ping")
    @commands.has_permissions(administrator=True)
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                logging.info("Command !ping used by - " + str(ctx.message.author))

                await ctx.send("Pong!", delete_after=15)
                logging.info("Response: Pong!")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")