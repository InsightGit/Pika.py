import discord
from discord.ext import commands
import asyncio
import random
import dataset
import pytimeparse

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def report(self, ctx, userToReport: discord.Member, reason: str):
        """Reports a user to the moderators."""
        config = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))["config"]
        for user in ctx.guild.members:
            if config.find_one(key="report_role") is None:
                role = discord.utils.get(user.roles, name="Mod")
            else:
                role = discord.utils.get(user.roles, name=config.find_one(key="report_role")["value"])
            if role:
                message = """**User Reported!**\n**Reportee**: {}\n**User Reported**: {}\n**Reason**: {}\n**Channel**: {}""".format(ctx.author.display_name, userToReport.display_name, reason, ctx.channel.name)
                await user.send(message)
        embed = discord.Embed(color=0xffff00, description="User reported! :spy:")
        await ctx.send(embed=embed)

    @commands.command()
    async def changenick(self, ctx, nick, user: discord.Member = None):
        """Starts a vote to change a users nickname"""
        config = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))["config"]
        if config.find_one(key="vote_cmd_status") is None or config.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
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
        if config.find_one(key="lvl1_vote_time") is None:
            sec = 60
            m, s = divmod(60, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(config.find_one(key="lvl1_vote_time")["value"])
            m, s = divmod(int(config.find_one(key="lvl1_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        if user == ctx.author:
            msg = await ctx.send("{} would like to change their nickname to **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(user.mention, nick, h, m, s))
        else:
            msg = await ctx.send("{} would like to change {}'s nickname to **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, nick, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            if user.nick is None:
                await msg.edit(content="The votes are in! **{}** is now known as **{}**!".format(user.name, nick))
            else:
                await msg.edit(content="The votes are in! **{}** (previous nickname: \"{}\") is now known as **{}**!".format(user.name, user.nick, nick))
            await user.edit(nick=nick)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {}'s nickname will not be changed... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author.mention))

    @commands.command()
    async def kick(self, ctx, user: discord.Member):
        """Starts a vote to kick a person"""
        config = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))["config"]
        if config.find_one(key="vote_cmd_status") is None or config.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
        if user == None:
            user = ctx.author
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl2_vote_time") is None:
            sec = 60
            m, s = divmod(300, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(config.find_one(key="lvl2_vote_time")["value"])
            m, s = divmod(int(config.find_one(key="lvl2_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        msg = await ctx.send("{} would like to kick **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been kicked".format(user.mention))
            await user.kick()
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be kicked... :(".format(user.mention))
        elif yes.count == no.count:
                await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def topic(self, ctx, *, topic):
        """Starts a vote to change this channel's topic"""
        config = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))["config"]
        o = []
        if config.find_one(key="vote_cmd_status") is None or config.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl1_vote_time") is None:
            sec = 60
            m, s = divmod(60, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(config.find_one(key="lvl1_vote_time")["value"])
            m, s = divmod(int(config.find_one(key="lvl1_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        msg = await ctx.send("{} would like to change this channel's topic to **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, topic, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            if ctx.channel.topic is None:
                await msg.edit(content="The votes are in! The channel topic has been changed to **{}**!".format(topic))
            else:
                await msg.edit(content="The votes are in! The channel topic has been changed to **{}**! (previous topic being: \"{}\")".format(topic, ctx.channel.topic))
            await ctx.channel.edit(topic=topic)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, the channel topic will not be changed... :(")
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def ban(self, ctx, user: discord.Member, days: int = None):
        """Start a vote to ban a user"""
        config = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))["config"]
        o = []
        if config.find_one(key="vote_cmd_status") is None or config.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl2_vote_time") is None:
            sec = 60
            m, s = divmod(300, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(config.find_one(key="lvl2_vote_time")["value"])
            m, s = divmod(int(config.find_one(key="lvl2_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        if days == None:
            msg = await ctx.send("{} would like to ban **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, h, m, s))
        else:
            msg = await ctx.send("{} would like to ban **{}** for **{} days**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, days, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
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
        """Start a vote to mute a user"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="vote_cmd_status") is None or table.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
        if table.find_one(key="lvl1_vote_time") is None:
            sec = 60
            m, s = divmod(60, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(table.find_one(key="lvl1_vote_time")["value"])
            m, s = divmod(int(table.find_one(key="lvl1_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        if minutes == None:
            msg = await ctx.send("{} would like to mute **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, h, m, s))
        else:
            msg = await ctx.send("{} would like to mute **{}** for **{} minutes**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, minutes, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been muted".format(user.mention))
            if table.find_one(key="modlog_channel") is not None or table.find_one(key="modlog_channel")["value"] != "off":
                mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
                embed = discord.Embed(color=0xffff00, description="User **{}** has been muted".format(user.name))
                embed.set_footer(text="User Mute", icon_url=user.avatar_url)
                await mlchannel.send(embed=embed)
            if table.find_one(key="muted_role")["value"] == "muted" or table.find_one(key="muted_role") == None:
                role = discord.utils.get(ctx.guild.roles, name="muted")
            else:
                role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
            await user.add_roles(role)
            if minutes != None:
                await asyncio.sleep(60 * minutes)
                embed = discord.Embed(color=0xffff00, description="User **{}** has been unmuted".format(user.name))
                embed.set_footer(text="User Unmute", icon_url=user.avatar_url)
                await mlchannel.send(embed=embed)
                await user.remove_roles(role)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be muted... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.command()
    async def unmute(self, ctx, user: discord.Member):
        """Start a vote to unmute a user"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="vote_cmd_status") is None or table.find_one(key="vote_cmd_status")["value"] == "off":
            await ctx.send("Sorry! The server owner has disabled the vote commands! Maybe ask them nicely to enable them?")
            return
        if table.find_one(key="lvl1_vote_time") is None:
            sec = 60
            m, s = divmod(60, 60)
            h, m = divmod(m, 60)
        else:
            sec = int(table.find_one(key="lvl1_vote_time")["value"])
            m, s = divmod(int(table.find_one(key="lvl1_vote_time")["value"]), 60)
            h, m = divmod(m, 60)
        msg = await ctx.send("{} would like to unmute **{}**! Let's vote, shall we? You have **{} hours, {} minutes, and {} seconds** to vote.".format(ctx.author.mention, user.mention, h, m, s))
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')
        await asyncio.sleep(sec)
        h = await ctx.channel.history(limit=500).flatten()
        msg = discord.utils.get(h, id=msg.id)
        yes = discord.utils.get(msg.reactions, emoji='👍')
        no = discord.utils.get(msg.reactions, emoji='👎')
        if yes.count > no.count:
            await msg.edit(content="The votes are in! {} has been unmuted".format(user.mention))
            if table.find_one(key="muted_role") is None:
                role = discord.utils.get(ctx.guild.roles, name="muted")
            else:
                role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
            if table.find_one(key="modlog_channel") is not None or table.find_one(key="modlog_channel")["value"] != "off":
                mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
                embed = discord.Embed(color=0xffff00, description="User **{}** has been unmuted".format(user.name))
                embed.set_footer(text="User Unmute", icon_url=user.avatar_url)
                await mlchannel.send(embed=embed)
            await user.remove_roles(role)
        elif no.count > yes.count:
            await msg.edit(content="The votes are in! Sadly, {} will not be unmuted... :(".format(user.mention))
        elif yes.count == no.count:
            await msg.edit(content="We got a tie! Sorry {}, not happening today!".format(ctx.author))

    @commands.group()
    async def room(self, ctx):
        """Room managment commands"""
        if ctx.invoked_subcommand is None:
            await ctx.send("you must use a valid subcommand :3")

    @room.command()
    async def create(self, ctx, *users: discord.Member):
        """Creates a room with the users that are specified"""
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
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["rooms"]
        table.insert(dict(channel=channel.id, role=role.id, owner=ctx.author.id))
        await ctx.send("Room created!")
        i = await channel.send("Send the various room commands to manage this room!")
        await i.pin()
        await channel.edit(topic="Owner: {}".format(ctx.author.mention))

    @room.command()
    async def add(self, ctx, *, username):
        """Adds a user to the room"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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
        """Removes a user from the room"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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

    @room.command(aliases=["delet"])
    async def delete(self, ctx):
        """Deletes a room"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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
        """Renames the room"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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
        """Changes the room topic"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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
        """Leaves a room"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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
        """Lists a room's members"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
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

    @commands.group()
    async def config(self, ctx):
        """Lists all the keys in the configuration"""
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        elif ctx.invoked_subcommand is None:
            await ctx.send("```Values you can edit using p!config set:\n\nmuted_role     This changes the muted role. Defaults to \"muted\"\n\nstarboard_channel     Changes what the starboard channel is named. Set to \"off\" to turn starboard off. Defaults to \"off\"\n\nlvl1_vote_time     Changes the vote time for the change nickname, mute, and channel topic Mod Vote commands, in the format of \"XdXhXmXs\" Defaults to \"1m\"\n\nlvl2_vote_time     Same thing as lvl1_vote_time, but for kicks and bans. Defaults to \"5m\"\n\nmodlog_channel     The name of the channel that the bot will post modlog messages to. Set to \"off\" to turn the modlog off. Defaults to \"off\"\n\nreport_role     Changes what role users need to have to recive reports. Defaults to \"Mod\"\n\nvote_cmd_status     Set to \"on\" or \"off\" if you would like to enable or disable the vote commands. Defaults to \"off\"\n\nwarns_to_kick     The amount of warns needed to kick a user. Defaults to \"2\"\nwarns_to_ban     The same thing as warns_to_kick, but for bans. Defaults to \"3\"```")

    @config.command()
    async def set(self, ctx, key, value):
        """Sets a value in the config"""
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
            table = db["config"]
            if key.lower() == "muted_role":
                if table.find_one(key="muted_role"):
                    table.update(dict(key="muted_role", value=value), ["key"])
                else:
                    table.insert(dict(key="muted_role", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "starboard_channel":
                if table.find_one(key="starboard_channel"):
                    table.update(dict(key="starboard_channel", value=value), ["key"])
                else:
                    table.insert(dict(key="starboard_channel", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "lvl1_vote_time":
                if table.find_one(key="lvl1_vote_time"):
                    table.update(dict(key="lvl1_vote_time", value=pytimeparse.parse(value)), ["key"])
                else:
                    table.insert(dict(key="lvl1_vote_time", value=pytimeparse.parse(value)))
                await ctx.send("Config updated!")
            elif key.lower() == "lvl2_vote_time":
                if table.find_one(key="lvl2_vote_time"):
                    table.update(dict(key="lvl2_vote_time", value=pytimeparse.parse(value)), ["key"])
                else:
                    table.insert(dict(key="lvl2_vote_time", value=pytimeparse.parse(value)))
                await ctx.send("Config updated!")
            elif key.lower() == "modlog_channel":
                if table.find_one(key="modlog_channel"):
                    table.update(dict(key="modlog_channel", value=value), ["key"])
                else:
                    table.insert(dict(key="modlog_channel", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "report_role":
                if table.find_one(key="report_role"):
                    table.update(dict(key="report_role", value=value), ["key"])
                else:
                    table.insert(dict(key="report_role", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "vote_cmd_status":
                if table.find_one(key="vote_cmd_status"):
                    table.update(dict(key="vote_cmd_status", value=value), ["key"])
                else:
                    table.insert(dict(key="vote_cmd_status", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "warns_to_kick":
                if table.find_one(key="warns_to_kick"):
                    table.update(dict(key="warns_to_kick", value=value), ["key"])
                else:
                    table.insert(dict(key="warns_to_kick", value=value))
                await ctx.send("Config updated!")
            elif key.lower() == "warns_to_ban":
                if table.find_one(key="warns_to_ban"):
                    table.update(dict(key="warns_to_ban", value=value), ["key"])
                else:
                    table.insert(dict(key="warns_to_ban", value=value))
                await ctx.send("Config updated!")
            else:
                await ctx.send("Hmm... that's not a valid key!")

    @config.command()
    async def get(self, ctx, key):
        """Gets whatever value in the config"""
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
            table = db["config"]
            if key.lower() == "muted_role":
                if table.find_one(key="muted_role"):
                    await ctx.send("``muted_role``'s current value is: ``{}``".format(table.find_one(key="muted_role")["value"]))
                else:
                    await ctx.send("``muted_role``'s current value is: ``muted``")
            elif key.lower() == "starboard_channel":
                if table.find_one(key="starboard_channel"):
                    await ctx.send("``starboard_channel``'s current value is: ``{}``".format(table.find_one(key="starboard_channel")["value"]))
                else:
                    await ctx.send("``starboard_channel``'s current value is: ``off``")
            elif key.lower() == "lvl1_vote_time":
                if table.find_one(key="lvl1_vote_time"):
                    await ctx.send("``lvl1_vote_time``'s current value is: ``{}``".format(table.find_one(key="lvl1_vote_time")["value"]))
                else:
                    await ctx.send("``lvl1_vote_time``'s current value is: ``1m``")
            elif key.lower() == "lvl2_vote_time":
                if table.find_one(key="lvl2_vote_time"):
                    await ctx.send("``lvl2_vote_time``'s current value is: ``{}``".format(table.find_one(key="lvl2_vote_time")["value"]))
                else:
                    await ctx.send("``lvl2_vote_time``'s current value is: ``5m``")
            elif key.lower() == "modlog_channel":
                if table.find_one(key="modlog_channel"):
                    await ctx.send("``modlog_channel``'s current value is: ``{}``".format(table.find_one(key="modlog_channel")["value"]))
                else:
                    await ctx.send("``modlog_channel``'s current value is: ``off``")
            elif key.lower() == "report_role":
                if table.find_one(key="report_role"):
                    await ctx.send("``report_role``'s current value is: ``{}``".format(table.find_one(key="report_role")["value"]))
                else:
                    await ctx.send("``report_role``'s current value is: ``Mod``")
            elif key.lower() == "vote_cmd_status":
                if table.find_one(key="vote_cmd_status"):
                    await ctx.send("``vote_cmd_status``'s current value is: ``{}``".format(table.find_one(key="vote_cmd_status")["value"]))
                else:
                    await ctx.send("``vote_cmd_status``'s current value is: ``off``")
            elif key.lower() == "warns_to_kick":
                if table.find_one(key="warns_to_kick"):
                    await ctx.send("``warns_to_kick``'s current value is: ``{}``".format(table.find_one(key="warns_to_kick")["value"]))
                else:
                    await ctx.send("``warns_to_kick``'s current value is: ``2``")
            elif key.lower() == "warns_to_ban":
                if table.find_one(key="warns_to_ban"):
                    await ctx.send("``warns_to_ban``'s current value is: ``{}``".format(table.find_one(key="warns_to_ban")["value"]))
                else:
                    await ctx.send("``warns_to_kick``'s current value is: ``2``")
            else:
                await ctx.send("Hmm... that's not a valid key!")
                return

    @config.command()
    async def reset(self, ctx, key):
        """Resets a value in the config"""
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
            table = db["config"]
            table.delete(key=key)
            await ctx.send("Config updated!")

    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            db = dataset.connect("sqlite:///servers/{}.db".format(after.guild.id))
            table = db["config"]
            if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
                return
            channel = discord.utils.get(after.guild.channels, name=table.find_one(key="modlog_channel")["value"])
            if before.nick is not None:
                if after.nick is not None:
                    embed = discord.Embed(color=0xffff00, description="**{}**'s nickname was changed to **{}**".format(before.nick, after.nick))
                else:
                    embed = discord.Embed(color=0xffff00, description="**{}**'s nickname was changed to **{}**".format(before.nick, after.name))
            else:
                if after.nick is not None:
                    embed = discord.Embed(color=0xffff00, description="**{}**'s nickname was changed to **{}**".format(before.name, after.nick))
                else:
                    embed = discord.Embed(color=0xffff00, description="**{}**'s nickname was changed to **{}**".format(before.nick, after.name))
            embed.set_footer(text="Nickname Change", icon_url=after.avatar_url)
            await channel.send(embed=embed)

    async def on_member_join(self, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has joined".format(member.name))
        embed.set_footer(text="User Join", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_remove(self, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has left".format(member.name))
        embed.set_footer(text="User Leave", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_ban(self, guild, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been banned".format(member.name))
        embed.set_footer(text="User Ban", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_unban(self, guild, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been unbanned".format(member.name))
        embed.set_footer(text="User Unban", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    @commands.command()
    async def fchangenick(self, ctx, nick, user: discord.Member):
        """Force changes a user's nickname"""
        if not ctx.author.guild_permissions.manage_nicknames:
            await ctx.send("Sorry! You must have the **Manage Nicknames** permission to use this command!")
            return
        if len(nick) > 32:
            embed = discord.Embed(color=0xffff00, description="Sorry, you reached the character limit on nicknames!")
            await ctx.send(embed=embed)
            return
        await user.edit(nick=nick)
        await ctx.send("Done!")

    @commands.command()
    async def fkick(self, ctx, user: discord.Member):
        """Force kicks a user"""
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("Sorry! You must have the **Kick Members** permission to use this command!")
            return
        await user.kick()
        await ctx.send("Done!")

    @commands.command()
    async def fban(self, ctx, user: discord.Member):
        """Force bans a user"""
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("Sorry! You must have the **Ban Members** permission to use this command!")
            return
        await user.ban()
        await ctx.send("Done!")

    @commands.command()
    async def fmute(self, ctx, user: discord.Member):
        """Force mutes a user"""
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="muted_role")["value"] == "muted" or table.find_one(key="muted_role") == None:
            role = discord.utils.get(ctx.guild.roles, name="muted")
        else:
            role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
        if table.find_one(key="modlog_channel") is not None or table.find_one(key="modlog_channel")["value"] != "off":
            mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
            embed = discord.Embed(color=0xffff00, description="User **{}** has been muted".format(user.name))
            embed.set_footer(text="User Mute", icon_url=user.avatar_url)
            await mlchannel.send(embed=embed)
        await user.add_roles(role)
        await ctx.send("Done!")

    @commands.command()
    async def funmute(self, ctx, user: discord.Member):
        """Force unmutes a user"""
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="muted_role") is None:
            role = discord.utils.get(ctx.guild.roles, name="muted")
        else:
            role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
        if table.find_one(key="modlog_channel") is not None or table.find_one(key="modlog_channel")["value"] != "off":
            mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
            embed = discord.Embed(color=0xffff00, description="User **{}** has been unmuted".format(user.name))
            embed.set_footer(text="User Unmute", icon_url=user.avatar_url)
            await mlchannel.send(embed=embed)
        await user.remove_roles(role)
        await ctx.send("Done!")

    @commands.command()
    async def warn(self, ctx, user: discord.Member, reason):
        """Warns a user"""
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["warns"]
        if not table.find_one(user=user.id):
            table.insert(dict(user=user.id, warns=1))
        else:
            table.update(dict(user=user.id, warns=table.find_one(user=user.id)["warns"]+1), ["user"])
        if db["config"].find_one(key="modlog_channel") is not None or db["config"].find_one(key="modlog_channel")["value"] != "off":
            mlchannel = discord.utils.get(ctx.guild.channels, name=db["config"].find_one(key="modlog_channel")["value"])
            embed = discord.Embed(color=0xffff00, description="User **{}** has been warned by {} for **{}**".format(user.name, ctx.author.name, reason))
            embed.set_footer(text="User Warn", icon_url=user.avatar_url)
            await mlchannel.send(embed=embed)
        await ctx.send("User warned!")
        await user.send("You have been warned for **{}**!\nYou now have **{}** warnings!".format(reason, table.find_one(user=user.id)["warns"]))
        if db["config"].find_one(key="warns_to_kick") is not None:
            if table.find_one(user=user.id)["warns"] == db["config"].find_one(key="warns_to_kick")["value"]:
                await user.send("Oops! You messed up one too many times, so you have been **kicked**! You *are* allowed to rejoin, but this time be REALLY careful, aight?")
                await user.kick()
        else:
            if table.find_one(user=user.id)["warns"] == 2:
                await user.send("Oops! You messed up one too many times, so you have been **kicked**! You *are* allowed to rejoin, but this time be REALLY careful, aight?")
                await user.kick()
        if db["config"].find_one(key="warns_to_ban") is not None:
            if table.find_one(user=user.id)["warns"] == db["config"].find_one(key="warns_to_ban")["value"]:
                await user.send("Oops! You messed up one too many times, so you have been **banned**! You *are not* allowed to rejoin, sadly.")
                await user.ban()
        else:
            if table.find_one(user=user.id)["warns"] == 3:
                await user.send("Oops! You messed up one too many times, so you have been **banned**! You *are not* allowed to rejoin, sadly.")
                await user.ban()

    @commands.command()
    async def warns(self, ctx, user: discord.Member):
        """Checks how many warns a user has"""
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["warns"]
        if not table.find_one(user=user.id):
            await ctx.send("This user has **0** warns!")
        else:
            await ctx.send("This user has **{}** warns!".format(table.find_one(user=user.id)["warns"]))

    async def toggleRole(self, user: discord.Member, role):
        if discord.utils.get(user.roles, name=role):
            await user.remove_roles(discord.utils.get(user.guild.roles, name=role))
            return False
        else:
            await user.add_roles(discord.utils.get(user.guild.roles, name=role))
            return True

    @commands.group(invoke_without_command=True)
    async def selfassign(self, ctx, *, role):
        """Gives yourself one of the self-assignable roles. If you have the role, run this command again to remove it"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["sar"]
        if table.find_one(name=role):
            if await Moderation.toggleRole(self, ctx.author, role) is True:
                await ctx.send("You now have the **{}** role!".format(role))
            elif await Moderation.toggleRole(self, ctx.author, role) is False:
                await ctx.send("You no longer have the **{}** role!".format(role))
        else:
            await ctx.send("Either that role dosen't exist, or it isn't self-assignable!")

    @selfassign.command()
    async def add(self, ctx, *, role):
        """Adds a role to the self-assignable roles list"""
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("Sorry! You must have the **Manage Roles** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["sar"]
        if table.find_one(name=role):
            await ctx.send("This role is already on the self-assignable roles list!")
            return
        table.insert(dict(name=role))
        await ctx.send("Role added!")

    @selfassign.command()
    async def remove(self, ctx, *, role):
        """Removes a role from the self-assignable roles list"""
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("Sorry! You must have the **Manage Roles** permission to use this command!")
            return
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["sar"]
        if not table.find_one(name=role):
            await ctx.send("This role is not on the self-assignable roles list!")
            return
        table.delete(name=role)
        await ctx.send("Role removed!")

    @selfassign.command()
    async def list(self, ctx):
        """List all roles in the self-assignable roles list"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["sar"]
        roles = []
        for r in table.all():
            roles.append(r["name"])
        if not roles:
            await ctx.send("No self-assignable roles found!")
            return
        embed = discord.Embed(color=0xffff00, title="Self-Assignable Roles", description="\n".join(roles))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Moderation(bot))
