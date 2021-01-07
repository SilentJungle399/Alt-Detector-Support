import discord
from discord.ext import commands
import random
import os
from datetime import datetime
import asyncio
import time

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = "as!", intents = intents)
start_time = time.time()
bot.remove_command('help')

@bot.event
async def on_connect():
	status1 = discord.Status.dnd
	Game = discord.Game("altdetector.tech | ad!help")
	await bot.change_presence(status = status1, activity = Game)
	print("The bot is ready!")
	print("Loading cogs . . .")

	for path, subdirs, files in os.walk("cogs"):
		for name in files:
			if name.endswith(".py"):
				name = os.path.join(name)[:-3]
				path = os.path.join(path).replace("/", ".")
				cog = path + "." + name
				try:
					bot.load_extension(cog)
					print(cog + " was loaded!")
				except Exception as e:
					print(e)
			else:
				continue

@bot.event
async def on_message(message):
	if message.author.bot:
		return
	await bot.process_commands(message)

@bot.command()
async def ping(ctx):
		before = time.monotonic()
		message = await ctx.send("Pong!")
		ping = (time.monotonic() - before) * 1000
		await message.edit(content=f"Pong! `{int(ping)} ms`")

token = "..."
bot.run(token, bot = True, reconnect = True)
