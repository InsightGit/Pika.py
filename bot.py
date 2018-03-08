import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='t!', description="""A multi-purpose Discord Bot created by ThatNerdyPikachu""", owner_id=124972333415792640)
cogs = ["cogs.internal", "cogs.economy", "cogs.fun", "cogs.moderation", "cogs.starboard", "cogs.utility"]

@bot.event
async def on_ready():
    for c in cogs:
        bot.load_extension(c)
    await bot.change_presence(activity=discord.Game(name="with pikas heartstrings ;-; | v1.1"))
    print("ready")

@bot.command()
async def about(ctx):
    """Shows info about the bot and who created it"""
    embed = discord.Embed(color=0xffff00, title="About", description="**Pika.py** v1.1\n\nCreated with love by ThatNerdyPikachu and friends, including:\nthe me_irl discord server\n2Hats\nMaster9000\nKronos\nMaki (for the name)\nFrederikTheDane")
    embed.set_footer(text="Thanks for checking me out! <3")
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    """Ping!"""
    await ctx.send("Pong!")

@bot.event
async def on_guild_join(guild):
    await guild.owner.send("Hey there server owner! My name is Pika.py, and I hope to be your good robot slave!\nHere are some things you have to do before I can be used:\n\n- Move the \"Pika.py\" role above every other role in your server (or above everyone you want it to be able to moderate)\n- Create a muted role, and give it whatever perms you want a muted user to have. (Move this above the roles aswell)\n- Edit the configuration! To help you out, p!config has a list of keys and example configurations to help you out!\n\nI hope you enjoy using me, and thanks for adding me in the first place!\n(By the way, if you ever need help with using the bot, join our Discord server at https://discord.gg/8vFPUhV, and we will be happy to assist you!)")

@bot.command()
@commands.is_owner()
async def reload(ctx):
    for c in cogs:
        bot.unload_extension(c)
        bot.load_extension(c)
    await ctx.send("Cogs reloaded!")

bot.run("NOPE (replace me)")
