import discord
from discord import app_commands
from discord.ext import commands
import importlib
import json
import os
import sys
import asyncio
from util import *

# load config with token and server
def load_config():
    global config
    env = os.getenv('BOT_ENV')
    config_file = 'config.json' if env == 'prod' else 'config.test.json'
    with open(config_file, encoding='utf8') as stream:
        config = json.load(stream)
    config = dotdict(config)
load_config()

# extend bot class
class MyBot(commands.Bot):
    def __init__(self, use_cogs):
        intents = discord.Intents.default()
        self.use_cogs = use_cogs
        self.synced = False
        super().__init__(command_prefix='>', intents=intents)

    async def on_ready(self):
        if not self.synced:
            self.tree.add_command(self.reload_cog)
            self.tree.add_command(self.restart_config)

            # import each Cog module and add the Cogs
            for cog in self.use_cogs:
                module = getattr(importlib.import_module(f'Cogs.{cog}'), cog)
                await self.add_cog(module(self, config))

            # sleep then sync with the guild
            await asyncio.sleep(1)
            await self.tree.sync()
            self.synced = True

        print('Bot ready to go!')

    @app_commands.command(name='reload_cog', description='Reload a Cog on the bot')
    async def reload_cog(self, interaction: discord.Interaction, cog: str):
        await interaction.response.defer(ephemeral=True)

        if cog in self.use_cogs:
            # remove the Cog from the bot
            removed = await self.remove_cog(cog)
            if not removed:
                await interaction.followup.send(f'Error unloading Cog `{cog}`')
                return

            # re-import the Cog module
            module = sys.modules[f'Cogs.{cog}']
            importlib.reload(module)
            # re-add the Cog class
            myclass = getattr(sys.modules[f'Cogs.{cog}'], cog)
            await self.add_cog(myclass(self, config))

            # sleep then sync
            await asyncio.sleep(1)
            await self.tree.sync(guild=discord.Object(id=config.server))

            await interaction.followup.send(f'Reloaded `{cog}`')
        else:
            await interaction.followup.send(f'Unknown Cog: {cog}')

    @app_commands.command(name='restart_config', description='Reload the bot config')
    async def restart_config(self, interaction):
        load_config()
        await interaction.response.send_message('Reloaded config', ephemeral=True)

# @reload_cog.autocomplete('cog')
# async def autocomplete_cog(interaction: discord.Interaction, current: str):
#     return [
#         app_commands.Choice(name=cog, value=cog) for cog in cogs if cog.startswith(current)
#     ]

bot = MyBot(['Greetings'])
bot.run(config.token)

