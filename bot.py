import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='p!', description="""a fun loving pikachu who turned into a robot.
its master is thatnerdypikachu. send help and ðŸ’™'s""", owner_id=124972333415792640)

@bot.event
async def on_ready():
    bot.load_extension("cogs.internal")
    bot.load_extension("cogs.economy")
    bot.load_extension("cogs.fun")
    bot.load_extension("cogs.factions")
    bot.load_extension("cogs.moderation")
    bot.load_extension("cogs.starboard")
    await bot.change_presence(game=discord.Game(name="with thunderbolts | v1.0 RC2"))
    print("ready")

bot.run("your token")
