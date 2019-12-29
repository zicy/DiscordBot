import configparser
import logging
import discord
from discord.ext import commands
from DiscordCommands import *
from BackgroundTask import *

## Read Config
config = configparser.ConfigParser()
config.sections()
config.read('settings.cfg')

## Define static values
TOKEN = config['BOT']['Token']
GUILD = int(config['BOT']['Guild'])
CHANNEL_ID = int(config['BOT']['Channel_ID'])
DEV = config['BOT']['Dev']

## Setup logger
logging.basicConfig(
        format='%(asctime)s [Discord] %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')


## Bot setup
DESCRIPTION = '''Im here to help'''
VERSION = "CraftersBot V0.1-dev"

Bot = commands.Bot(command_prefix="!", description=DESCRIPTION, case_insensitive=True)


@Bot.event
async def on_ready():
    logging.info("Starting Bot")
    logging.info("Version: " + VERSION)
    logging.info("Username: " + Bot.user.name)
    logging.info("Bot ID: " + str(Bot.user.id))
    logging.info("---[ Connected Servers]---")
    for Guild in Bot.guilds:
        logging.info("Guild ID: " + str(Guild.id) + " Name: " + Guild.name + " Member Count: " + str(Guild.member_count))
    logging.info("---[ Bot Started ]---")
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=VERSION, type=1))
    logging.info("")

    Bot.loop.create_task(MinecraftServerMonitor.Background_Monitor_Task(Bot, logging, config, CHANNEL_ID))

## Commands

# !Ping
PingCommand.run(Bot, GUILD, CHANNEL_ID)
logging.info("Loaded: PingCommand - Ping/Pong")

# !Rcon <server> <command>
RconCommand.run(Bot, GUILD, CHANNEL_ID)
#logging.info("Loaded: RconCommand")

# !Restart <server> [delay]
RestartCommand.run(Bot, GUILD, CHANNEL_ID)
#logging.info("Loaded: RestartCommand")

# !Status <server|all>
MinecraftStatusCommand.run(Bot, logging, config, GUILD, CHANNEL_ID)
logging.info("Loaded: MinecraftStatusCommand - Get status about Minecrafter servers")

# !SelfUpdate
SelfUpdateCommand.run(Bot, logging, config, DEV)
logging.info("Loaded: SelfUpdateCommand - Update to lates release on from Github")

# !SelfStop
SelfStopCommand.run(Bot, logging)
logging.info("Loaded: SelfStopCommand - Stop/ restart the bot")


## Start Discord Bot
Bot.run(TOKEN)