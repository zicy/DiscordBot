### Status Script
import json
import socket
import sys
import traceback
### Status Script

import discord
import asyncio
from discord.ext import tasks, commands
### Status Script
from mcstatus import MinecraftServer
from datetime import datetime
### Status Script


async def Background_Monitor_Task(self, logging, config, CHANNEL_ID):
    await self.wait_until_ready()
    channel = self.get_channel(int(config['BOT']['AdminNotificationChannel']))

    while not self.is_closed():

        ip = "127.0.0.1"
        game_port = 25565

        server = MinecraftServer.lookup("{0}:{1}".format(ip, game_port))
        status = server.status()
        players_online=format(status.players.online)
        players_max=format(status.players.max)

        server_status = "{}/{} online på crafters.dk".format(players_online, players_max)

        logging.info("Updating bot activity to: {}".format(server_status))
        await self.change_presence(status=discord.Status.idle, activity=discord.Activity(name=server_status, type=3))

        await asyncio.sleep(int(config['ACTIVITY']['Update'])) # task runs every xx seconds