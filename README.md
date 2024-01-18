# cog-bot-framework

A discord.py bot framework I'm trying to develop to have reloadable Cogs for hotswap changes without restarting the bot.

I have no idea if this is the right way to do any of this, but it works pretty well!

One gotcha is that if modules imported by the Cog are changed, they need to be re-imported!
