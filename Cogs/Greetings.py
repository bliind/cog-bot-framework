import discord
import random
from discord import app_commands
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot, config):
        self.bot = bot
        self.config = config
        self.server = discord.Object(id=config.server)

    # add commands to the tree on load
    async def cog_load(self):
        self.bot.tree.add_command(self.hello, guild=self.server)

    # remove commands from the tree on load
    async def cog_unload(self):
        self.bot.tree.remove_command('hello', guild=self.server)

    # says hellos
    @app_commands.command(name='hello', description='Say Hello')
    async def hello(self, interaction: discord.Interaction):
        hellos = ['Hello', 'Hey there', 'OMG HI', 'Sup']
        await interaction.response.send_message(random.choice(hellos))

    # says goodbyes
    @app_commands.command(name='goodbye', description='Says goodbye')
    async def goodbye(self, interaction: discord.Interaction):
        goodbyes = ['Later', 'Goodbye', 'Farewell', 'Peace']
        await interaction.response.send_message(random.choice(goodbyes))

    # listens for mentions of the bot
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if str(self.bot.user.id) in message.content:
            await message.channel.send('What you say about me??')
