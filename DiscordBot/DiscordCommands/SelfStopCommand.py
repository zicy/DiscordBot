import discord
from discord.ext import commands


def run(Bot, logging):

    #Bot = self.bot

    @Bot.command(name="selfstop")
    @commands.has_permissions(administrator=True)
    async def _cmd(ctx):
        logging.info("Command !selfstop used by - " + str(ctx.message.author))

        await ctx.send("Stopping . . .")
        logging.info("Stopping . . .")
        await ctx.bot.close()

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")
    
