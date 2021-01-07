from discord.ext import commands
import sqlite3
import re

class on_message(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.db = sqlite3.connect("main.sqlite")
		self.cursor = self.db.cursor()
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS mass_mentions(
				user TEXT,
				warns TEXT,
				kick TEXT			
			)
		""")

	async def process_warn(self, member, reason):
		sql = "SELECT * FROM mass_mentions WHERE user=?"
		self.cursor.execute(sql, (member.id, ))
		result = self.cursor.fetchone()
		if result:
			if int(result[1]) > 2:
				await self.process_action(member, reason)
			else:
				sql = "UPDATE mass_mentions SET warns=? WHERE user=?"
				val = (int(result[1]) + 1, member.id)
				self.cursor.execute(sql, val)
				self.db.commit()
		else:
			sql = "INSERT INTO mass_mentions(user, warns, kick) VALUES(?, ?, ?)"
			val = (member.id, 1, 0)
			self.cursor.execute(sql, val)
			self.db.commit()

	async def process_action(self, member, reason):
		sql = "SELECT * FROM mass_mentions WHERE user=?"
		self.cursor.execute(sql, (member.id, ))
		result = self.cursor.fetchone()
		if int(result[2]) == 0:
			await member.send(f"You got kicked from Alt Detector Support server. Reason: `{reason}`")
			await member.kick(reason = reason)
			sql = "UPDATE mass_mentions SET kick=? WHERE user=?"
			val = (1, member.id)
			self.cursor.execute(sql, val)
			self.db.commit()
		elif int(result[2]) == 1:
			await member.send(f"You got banned from Alt Detector Support server. Reason: `{reason}`")
			await member.ban(reason = reason)

	@commands.Cog.listener()
	async def on_message(self, message):
		if len(message.mentions) > 3:
			await self.process_warn(message.author, "Mass ping.")



def setup(bot):
	bot.add_cog(on_message(bot))