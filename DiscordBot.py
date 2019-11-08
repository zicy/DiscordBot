import configparser
import discord
from discord.ext import commands
from DiscordCommands import *

config = configparser.ConfigParser()
config.sections()
config.read('settings.cfg')

TOKEN = config['BOT']['Token']
GUILD = config['BOT']['Guild']
CHANNEL_ID = config['BOT']['Channel_ID']
DEV = config['BOT']['Dev']

DESCRIPTION = '''Im here to help'''
VERSION = "CraftersBot V0.1-dev"

Bot = commands.Bot(command_prefix="!", description=DESCRIPTION,case_insensitive=True)

@Bot.event
async def on_ready():
    print("Starting Bot,")
    print("Version: " + VERSION)
    print("Username: " + Bot.user.name)
    print("Bot ID: " + str(Bot.user.id))
    print("---[ Connected Servers]---")
    for Guild in Bot.guilds:
        print("Guild ID: " + str(Guild.id) + " Name: " + Guild.name + " Member Count: " + str(Guild.member_count))
    print("---[ Bot Started ]---")
    await Bot.change_presence(status=discord.Status.idle, activity=discord.Activity(name=VERSION, type=1))
    print("")


# !Ping
PingCommand.run(Bot, GUILD, CHANNEL_ID)

# !Rcon [server] command
RconCommand.run(Bot, GUILD, CHANNEL_ID)

# !Restart <server> <delay>
RestartCommand.run(Bot, GUILD, CHANNEL_ID)

# !Status [server]
StatusCommand.run(Bot, GUILD, CHANNEL_ID)

# !SelfUpdate
SelfUpdateCommand.run(Bot, config['UPDATE']['Url'], config['UPDATE']['SaveFile'], DEV)

# !SelfStop
SelfStopCommand.run(Bot)




Bot.run(TOKEN)