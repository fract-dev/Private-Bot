import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

EXCLUDED_CHANNELS = ['rules', 'welcome', 'announcements', 'chat']

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

@bot.command()
@commands.has_permissions(manage_channels=True)
async def private(ctx):
    guild = ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    for channel in guild.channels:
        try:
            if channel.name.lower() in EXCLUDED_CHANNELS:
                await ctx.send(f"Skipping channel: {channel.name}")
                continue
            await channel.edit(overwrites=overwrites)
            print(f"Privated: {channel.name}")
        except Exception as e:
            print(f"Could not private {channel.name}: {e}")
            await ctx.send(f"❌ Could not private `{channel.name}`: {e}")

    await ctx.send("🔒 Server lockdown complete (excluding protected channels).")

bot.run(os.getenv("DISCORD_TOKEN"))
