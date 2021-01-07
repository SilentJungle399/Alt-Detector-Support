from discord.ext import commands

class member_join_leave(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_join(self, member):
		await member.add_roles(member.guild.get_role(772526051150266368))

def setup(bot):
	bot.add_cog(member_join_leave(bot))