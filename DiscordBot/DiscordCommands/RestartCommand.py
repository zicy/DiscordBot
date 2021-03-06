import discord
import os
from discord.ext import commands


def run(Bot, logging, GUILD, CHANNEL_ID):

    #Bot = self.bot

    @Bot.command(name="restart")
    @commands.has_permissions(administrator=True)
    async def _cmd(ctx):
        if ctx.message.guild.id == int(GUILD):
            if ctx.message.channel.id == int(CHANNEL_ID):
                logging.info("Command !restart used by - " + str(ctx.message.author))
                cmd = "Restart.sh"
                if os.path.exists(cmd):
                    await ctx.send("Running " + cmd +  " ...")
                    logging.info("Response: Ussage: !status <server> \nExample: !server novus")
                else:        
                    await ctx.send("Error! " + cmd + " don't exist")
                    logging.info("Response: Ussage: !status <server> \nExample: !server novus")

    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send("Unknown error!")
            logging.error("Unknown error!")