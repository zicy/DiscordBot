import configparser
import logging
import discord
from discord.ext import commands
from DiscordCommands import *
from BackgroundTask import *

config = configparser.ConfigParser()
config.sections()
config.read('settings.cfg')

TOKEN = config['BOT']['Token']
GUILD = int(config['BOT']['Guild'])
CHANNEL_ID = int(config['BOT']['Channel_ID'])
DEV = config['BOT']['Dev']

logging.basicConfig(
        format='%(asctime)s [Discord] %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')


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

def syslog():
    pass

# !Ping
PingCommand.run(Bot, GUILD, CHANNEL_ID)

# !Rcon <server> <command>
RconCommand.run(Bot, GUILD, CHANNEL_ID)

# !Restart <server> [delay]
RestartCommand.run(Bot, GUILD, CHANNEL_ID)

# !Status <server|all>
MinecraftStatusCommand.run(Bot, config, GUILD, CHANNEL_ID)

# !SelfUpdate
SelfUpdateCommand.run(Bot, logging, config['UPDATE']['Url'], config['UPDATE']['SaveFile'], DEV)

# !SelfStop
SelfStopCommand.run(Bot, logging)



Bot.run(TOKEN)