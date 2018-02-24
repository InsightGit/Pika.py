import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='p!', description="""A multi-purpose Discord Bot created by ThatNerdyPikachu""", owner_id=124972333415792640)

@bot.event
async def on_ready():
    bot.load_extension("cogs.internal")
    bot.load_extension("cogs.economy")
    bot.load_extension("cogs.fun")
    bot.load_extension("cogs.factions")
    bot.load_extension("cogs.moderation")
    bot.load_extension("cogs.starboard")
    await bot.change_presence(game=discord.Game(name="with thunderbolts | v1.0"))
    print("ready")
    
@bot.command()
async def about(ctx):
    embed = discord.Embed(color=0xffff00, title="About", description="**Pika.py** v1.0\n\nCreated with love by ThatNerdyPikachu and friends, including:\nthe me_irl discord server\n2Hats\nMaster9000\nKronos\nMaki (for the name)\nFrederikTheDane")
    embed.set_footer(text="Thanks for checking me out! <3")
    await ctx.send(embed=embed)

bot.run("your token")
