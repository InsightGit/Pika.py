import discord
from discord.ext import commands
import asyncio
import random
import dataset

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx, userToReport: discord.Member, reason: str):
        """Reports a user to the moderators."""
        for user in ctx.guild.members:
            if discord.utils.get(user.roles, name="Mod"):
                message = """**User Reported!**\n**Reportee**: {}\n**User Reported**: {}\n**Reason**: {}\n**Channel**: {}""".format(ctx.author.display_name, userToReport.display_name, reason, ctx.channel.name)
                await user.send(message)
        embed = discord.Embed(color=0xffff00, description="User reported! :spy:")
        await ctx.send(embed=embed)

    @commands.command()
    async def changenick(self, ctx, nick, user: discord.Member = None):
        if len(nick) > 32:
            embed = discord.Embed(color=0xffff00, description="Sorry, you reached the character limit on nicknames!")
            await ctx.send(embed=embed)
            return
        if user == None:
            user = ctx.author
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        if user == ctx.author:
            msg = await ctx.send("{} would like to change their nickname to **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(user.mention, nick, min, sec))
        else:
            msg = await ctx.send("{} would like to change {}'s nickname to {}! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, nick, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} is now known as {}!".format(user.mention, nick))
            await user.edit(nick=nick)
        elif no.count > yes.count:
            await msg.edit(
                content="The votes are in! Sadly, {}'s nickname will not be changed... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(user.mention))

    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        if user == None:
            user = ctx.author
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        msg = await ctx.send("{} would like to kick **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been kicked".format(user.mention))
            await user.kick()
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {}'s will not be kicked... :(".format(user.mention))
        elif yes.count == no.count:
                await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def topic(self, ctx, *, topic):
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        msg = await ctx.send("{} would like to change this channel's topic to **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, topic, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! The channel topic has been changed to **{}**!".format(topic))
            await ctx.channel.edit(topic=topic)
        elif no.count > yes.count:
            await msg.edit(
                content="The votes are in! Sadly, the channel topic will not be changed... :(")
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def ban(self, ctx, user: discord.Member, days: int = None):
        if user == None:
            user = ctx.author
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        if days == None:
            msg = await ctx.send("{} would like to ban **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, min, sec))
        else:
            msg = await ctx.send("{} would like to ban **{}** for **{} days**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, days, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been banned".format(user.mention))
            await user.ban()
            if days != None:
                await asyncio.sleep((60 * 60) * 24 * days)
                await user.unban()
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be banned... :(".format(user.mention))
        elif yes.count == no.count:
                await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def mute(self, ctx, user: discord.Member, minutes: int = None):
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        if minutes == None:
            msg = await ctx.send("{} would like to mute **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, min, sec))
        else:
            msg = await ctx.send("{} would like to mute **{}** for **{} minutes**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, minutes, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been muted".format(user.mention))
            role = discord.utils.get(ctx.guild.roles, name="muted")
            await user.add_roles(role)
            if minutes != None:
                await asyncio.sleep(60 * minutes)
                await user.remove_roles(role)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be muted... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def unmute(self, ctx, user: discord.Member):
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        sec = 30 / len(o) - 30 // len(o)
        min = 30 // len(o)
        sec = round(sec)
        msg = await ctx.send("{} would like to unmute **{}**! Let's vote, shall we? You have **{} minutes and {} seconds** to vote.".format(ctx.author.mention, user.mention, min, sec))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec + (min * 60))
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been unmuted".format(user.mention))
            role = discord.utils.get(ctx.guild.roles, name="muted")
            await user.remove_roles(role)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be unmuted... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.group()
    async def room(self, ctx):
        if ctx.invoked_subcommand == None:
            await ctx.send("you must use a subcommand :3")

    @room.command()
    async def create(self, ctx, *users: discord.Member):
        name = "room_{}".format(random.randint(1000, 9999))
        role = await ctx.guild.create_role(name=name)
        if discord.utils.get(ctx.guild.channels, name="Rooms"):
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=discord.utils.get(ctx.guild.channels, name="Rooms"))
        else:
            category = await ctx.guild.create_category(name="Rooms")
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites, category=category)
        await ctx.author.add_roles(role)
        for m in users:
            await m.add_roles(role)
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        table.insert(dict(channel=channel.id, role=role.id, owner=ctx.author.id))
        await ctx.send("creat0red")
        i = await channel.send("send teh room commands comrade")
        await i.pin()
        await channel.edit(topic="Owner: {}".format(ctx.author.mention))

    @room.command()
    async def add(self, ctx, *, username):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] != ctx.author.id:
            await ctx.send("you are not the owner, stop trying to trick me!")
        else:
            role = discord.utils.get(ctx.guild.roles, id=table.find_one(channel=ctx.channel.id)["role"])
            user = ctx.guild.get_member_named(username)
            if discord.utils.get(user.roles, name=role.name):
                await ctx.send("this user is already in the room!")
                return
            await user.add_roles(role)
            await ctx.send("added!")

    @room.command()
    async def remove(self, ctx, user: discord.Member):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] != ctx.author.id:
            await ctx.send("you are not the owner, stop trying to trick me!")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, id=table.find_one(channel=ctx.channel.id)["role"])
            if not discord.utils.get(user.roles, name=role.name):
                await ctx.send("this user is not in the room!")
                return
            await user.remove_roles(role)
            await ctx.send("removed!")

    @room.command()
    async def delete(self, ctx):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] != ctx.author.id:
            await ctx.send("you are not the owner, stop trying to trick me!")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, id=table.find_one(channel=ctx.channel.id)["role"])
            table.delete(channel=ctx.channel.id)
            await ctx.channel.delete()
            await role.delete()

    @room.command()
    async def rename(self, ctx, name):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] != ctx.author.id:
            await ctx.send("you are not the owner, stop trying to trick me!")
            return
        else:
            await ctx.channel.edit(name=name)
            await ctx.send("done")

    @room.command(name="topic")
    async def _topic(self, ctx, *, topic):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] != ctx.author.id:
            await ctx.send("you are not the owner, stop trying to trick me!")
            return
        else:
            await ctx.channel.edit(topic="{} | Owner: {}".format(topic, ctx.author.mention))
            await ctx.send("done")

    @room.command()
    async def leave(self, ctx):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        elif table.find_one(channel=ctx.channel.id)["owner"] == ctx.author.id:
            await ctx.send("nonono, you are the owner! you cant leave your own room!")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, id=table.find_one(channel=ctx.channel.id)["role"])
            await ctx.author.remove_roles(role)
            await ctx.send("done")

    @room.command()
    async def members(self, ctx):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["rooms"]
        if not table.find_one(channel=ctx.channel.id):
            await ctx.send("use this in a room please")
            return
        else:
            role = discord.utils.get(ctx.guild.roles, id=table.find_one(channel=ctx.channel.id)["role"])
            ml = []
            for m in ctx.guild.members:
                if discord.utils.get(m.roles, id=role.id):
                    ml.append(m.display_name)
                else:
                    continue
            await ctx.send("members of this room: ```{}```".format(", ".join(ml)))

def setup(bot):
    bot.add_cog(Moderation(bot))
