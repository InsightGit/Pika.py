import discord
from discord.ext import commands
import random
import dataset

class Factions:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx):
        """Gives you a random Factions group"""
        if discord.utils.get(ctx.author.roles, name="Stalinist") is not None or discord.utils.get(ctx.author.roles, name="Trotskyist"):
            embed = discord.Embed(color=0xffff00, description="Don't try to fool me! You're already a member of a faction!")
            await ctx.send(embed=embed)
            return
        stal = discord.utils.get(ctx.guild.roles, name="Stalinist")
        trot = discord.utils.get(ctx.guild.roles, name="Trotskyist")
        roles = [stal, trot, stal, trot]
        roleToAssign = random.choice(roles)
        await ctx.author.add_roles(roleToAssign, atomic=True)
        embed = discord.Embed(color=0xffff00, description="You are now a **{}**!".format(roleToAssign.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def gpoints(self, ctx):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        s = []
        t = []
        for user in ctx.guild.members:
            if discord.utils.get(user.roles, name="Stalinist"):
                table = db["xp"]
                data = table.find_one(user=user.id)
                s.append(data["xp"])
            elif discord.utils.get(user.roles, name="Trotskyist"):
                table = db["xp"]
                data = table.find_one(user=user.id)
                t.append(data["xp"])
            else:
                continue
        embed = discord.Embed(title="Faction Points", color=0xffff00)
        embed.add_field(name="Stalinism", value=sum(s), inline=True)
        embed.add_field(name="Trotskyism", value=sum(t), inline=True)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Factions(bot))