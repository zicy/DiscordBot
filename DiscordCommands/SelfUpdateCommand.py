import discord
from discord.ext import commands
import urllib.request
import zipfile
import os


def run(Bot, logging, URL, SAVEFILE, DEV):

    #Bot = self.bot

    @Bot.command(name="selfupdate")
    async def _cmd(ctx):
        

        # Fetch update ZIP
        logging.info("Beginning file download with urllib2...")
        await ctx.send("Beginning file download with urllib2...")
        urllib.request.urlretrieve(URL, SAVEFILE)

        # Unzip update.zip
        logging.info("Beginning unzip with zipfile...")
        await ctx.send("Beginning unzip with zipfile...")
        with zipfile.ZipFile(SAVEFILE, 'r') as zip_ref:
               zip_ref.extractall()
        
        # Move file from extracted folder to current folder
        if DEV == "False":
            logging.info("cp -r DiscordBot-master/* .")
            os.system("cp -r DiscordBot-master/* .")
         
        # Start new DiscordBot
        logging.info("Done")
        await ctx.send("Done")
        logging.info("Restarting . . .")
        await ctx.send("Restarting . . .")
        await ctx.bot.close()
        if DEV == "False":
            logging.info("DiscordBot.py")
            os.system("DiscordBot.py")


    @_cmd.error
    async def _cmd_error(ctx, error):
        if isinstance(error, commands.BadArgument):
            logging.error("Unknown error!")
            await ctx.send("Unknown error!")
    
