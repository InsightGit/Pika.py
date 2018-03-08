import discord
from discord.ext import commands
import dataset

class Utility:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
        """Gets a users avatar. If no user is specified, your avatar will be sent instead"""
        if user == None:
            user = ctx.author
        await ctx.send(user.avatar_url)

    @commands.command()
    async def serverinfo(self, ctx):
        """Shows info about the current server"""
        embed = discord.Embed(color=0xffff00)
        embed.add_field(name="Name", value=ctx.guild.name, inline=True)
        embed.add_field(name="Owner", value="{}#{}".format(ctx.guild.owner.name, ctx.guild.owner.discriminator), inline=True)
        embed.add_field(name="Created On", value="{}/{}/{}".format(ctx.guild.created_at.month, ctx.guild.created_at.day, ctx.guild.created_at.year), inline=True)
        embed.add_field(name="Member Count", value=len(ctx.guild.members), inline=True)
        embed.add_field(name="Channel Count", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def profile(self, ctx, user: discord.Member = None):
        """Shows a users profile. If no user is specified, your profile will be showed instead."""
        if user is None:
            user = ctx.author
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["profiles"]
        if table.find_one(user=user.id) is not None:
            if "color" in table.find_one(user=user.id):
                hex_str = "0x" + table.find_one(user=user.id)["color"]
                hex_int = int(hex_str, 16)
                embed = discord.Embed(color=hex_int)
            else:
                embed = discord.Embed(color=0xffff00)
        else:
            embed = discord.Embed(color=0xffff00)
        embed.add_field(name="Name", value="{}#{}".format(user.name, user.discriminator), inline=True)
        if user.nick is not None:
            embed.add_field(name="Nickname", value=user.nick, inline=True)
        else:
            embed.add_field(name="Nickname", value="None found!", inline=True)
        embed.add_field(name="Joined", value="{}/{}/{}".format(user.joined_at.month, user.joined_at.day, user.joined_at.year), inline=True)
        embed.add_field(name="Account Created", value="{}/{}/{}".format(user.created_at.month, user.created_at.day, user.created_at.year), inline=True)
        if table.find_one(user=user.id) is not None:
            if "description" in table.find_one(user=user.id):
                embed.add_field(name="Description", value=table.find_one(user=user.id)["description"], inline=True)
            else:
                embed.add_field(name="Description", value="None set!", inline=True)
        else:
            embed.add_field(name="Description", value="None set!", inline=True)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @profile.command()
    async def description(self, ctx, *, description):
        """Sets your profile description"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["profiles"]
        if table.find_one(user=ctx.author.id):
            table.update(dict(user=ctx.author.id, description=description), ["user"])
        else:
            table.insert(dict(user=ctx.author.id, description=description))
        await ctx.send("Profile updated!")

    @profile.command()
    async def color(self, ctx, *, color):
        """Sets your profile color in hex. (Note, if your hex code has a \"0x\" or a '#', please remove it, otherwise the embed will fail.)"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["profiles"]
        if table.find_one(user=ctx.author.id):
            table.update(dict(user=ctx.author.id, color=color.lower()), ["user"])
        else:
            table.insert(dict(user=ctx.author.id, color=color.lower()))
        await ctx.send("Profile updated!")

def setup(bot):
    bot.add_cog(Utility(bot))
