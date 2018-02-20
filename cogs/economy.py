import discord
from discord.ext import commands
import dataset
import random

class Economy:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        db = dataset.connect("sqlite:///{}.db".format(message.guild.id))
        for user in message.guild.members:
            if db["xp"].find_one(user=user.id):
                continue
            else:
                db["xp"].insert(dict(user=user.id, xp=0))

        users = db["xp"].all()
        for user in users:
            if user["xp"] < 0:
                db["xp"].update(dict(user=user["user"], xp=0), ["user"])

        cmdCheck = ['!', '-', '?', '_', '%']
        for prefix in cmdCheck:
            if message.content.startswith(prefix):
                return

        if message.author.bot == True:
            return
        table = db["xp"]
        data = table.find_one(user=message.author.id)
        table.update(dict(user=message.author.id, xp=data["xp"]+1), ["user"])

    @commands.command()
    async def xp(self, ctx, user: discord.Member = None):
        """Check a users XP!"""
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        if user == None:
            user = ctx.author
        elif user == self.bot.user:
            embed = discord.Embed(description="*I* have infinite XP! You silly little user...", color=0xffff00)
            await ctx.send(embed=embed)
            return
        elif user.id == 162952008712716288:
            embed = discord.Embed(color=0xffff00, description="Master9000 broke me. He has ***I N F I N I T E***  XP now!")
            await ctx.send(embed=embed)
            return

        table = db["xp"]
        data = table.find_one(user=user.id)
        xp = data["xp"]
        embed = discord.Embed(title="{}'s XP".format(user.display_name), description="This user has {} XP points!".format(xp), color=0xffff00)
        embed.set_author(name="Pika.py",
                         icon_url =
                         "https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def rr(self, ctx, bet: int):
        """Russian Roulette! Bet some XP!"""
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["xp"]
        data = table.find_one(user=ctx.author.id)
        if bet < 10:
            embed = discord.Embed(color=0xffff00, description="You must bet at least 10 XP!")
            await ctx.send(embed=embed)
            return
        elif bet > data["xp"]:
            embed = discord.Embed(color=0xffff00, description="You cannot bet more XP than you have, silly!")
            await ctx.send(embed=embed)
            return
        num = random.randint(1, 3)
        print(num)
        if num == 3:
            table = db["xp"]
            won = bet*3
            data = table.find_one(user=ctx.author.id)
            table.update(dict(user=ctx.author.id, xp=data["xp"]+won), ["user"])
            ud = table.find_one(user=ctx.author.id)
            embed = discord.Embed(color=0xffff00, description="Congrats! You made {} XP! Your total is now {}!".format(won, ud["xp"]))
            await ctx.send(embed=embed)
        else:
            table = db["xp"]
            data = table.find_one(user=ctx.author.id)
            table.update(dict(user=ctx.author.id, xp=data["xp"]-bet), ["user"])
            data = table.find_one(user=ctx.author.id)
            embed = discord.Embed(color=0xffff00, description="Oh no! You lost {} XP! Your total XP is now {}! Better luck next time!".format(bet, data["xp"]))
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def setxp(self, ctx, user: discord.Member, xp):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["xp"]
        table.update(dict(user=user.id, xp=xp), ["user"])
        await ctx.send("done")

def setup(bot):
    bot.add_cog(Economy(bot))