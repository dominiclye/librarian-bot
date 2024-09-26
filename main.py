from discord.ext import commands
from discord.ext.commands import has_permissions
import discord
import os, dotenv

from utils.config import load_json_settings
from dbActions.SettingsActions import SettingsActions
import motor.motor_asyncio



dotenv.load_dotenv(".env")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="s?", intents=intents)
bot.color = 0xffe2e0
bot.settings_cache = {}

uri = os.getenv("DB_URI")
defaults = load_json_settings()
bot.client = motor.motor_asyncio.AsyncIOMotorClient(uri)
bot.guilds_client = bot.client["study-bot"]

@bot.event
async def on_ready():
    bot.settings_actions = SettingsActions(bot.guilds_client["guilds"])
    await bot.change_presence(activity=discord.Game(name=f"s?help", type=2))
    
    for guild in bot.guilds:
        server_settings = await bot.settings_actions.get_guild(guild.id)
        if server_settings is None:
            await bot.settings_actions.add_guild(guild.id, defaults)
            bot.settings_cache[guild.id] = defaults
            print(f"Added {guild.name} to the database with default settings.")
        else:
            bot.settings_cache[guild.id] = server_settings['settings']
            print(f"Server {guild.name} already exists in the database.")
    
    await setup(bot)

async def on_guild_join(guild):
    server_settings = await bot.settings_actions.get_guild(guild.id)
    
    if server_settings is None:
        await bot.settings_actions.add_guild(guild.id, defaults)
        bot.settings_cache[guild.id] = defaults
        print(f"Added {guild.name} to the database with default settings.")
    else:
        bot.settings_cache[guild.id] = server_settings['settings']
        print(f"Server {guild.name} already exists in the database.")

@bot.command()
async def reload(ctx, *, name: str):
    try:
        await bot.reload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send('Reloaded ' + name)

@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, *, name: str):
    try:
        await bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send('Loaded ' + name)

@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, *, name: str):
    try:
        await bot.unload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send('Unloaded ' + name)
    
cogs = ["cogs.VoiceCommands", "cogs.SettingsCommands", "cogs.ErrorHandling"]

async def setup(bot):
    for cog in cogs:
        try:
            print(cog)
            await bot.load_extension(cog)
        except Exception as e:
            print(f"An error occured: {e}")

bot.run(os.getenv("BOT_TOKEN"))