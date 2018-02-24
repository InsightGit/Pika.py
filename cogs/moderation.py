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
        for user in ctx.guild.members:
            if discord.utils.get(user.roles, name="Mod"):
                message = """**User Reported!**\n**Reportee**: {}\n**User Reported**: {}\n**Reason**: {}\n**Channel**: {}""".format(ctx.author.display_name, userToReport.display_name, reason, ctx.channel.name)
                await user.send(message)
        embed = discord.Embed(color=0xffff00, description="User reported! :spy:")
        await ctx.send(embed=embed)

    @commands.command()
    async def changenick(self, ctx, nick, user: discord.Member = None):
        config = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))["config"]
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
        if config.find_one(key="lvl1_vote_time") is None or config.find_one(key="lvl1_vote_time")["value"] == "1m":
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
        config = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))["config"]
        if user == None:
            user = ctx.author
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl2_vote_time") is None or config.find_one(key="lvl1_vote_time")["value"] == "5m":
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
        config = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))["config"]
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl1_vote_time") is None or config.find_one(key="lvl1_vote_time")["value"] == "1m":
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
        config = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))["config"]
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if config.find_one(key="lvl2_vote_time") is None or config.find_one(key="lvl1_vote_time")["value"] == "5m":
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
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["config"]
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if table.find_one(key="lvl1_vote_time") is None or table.find_one(key="lvl1_vote_time")["value"] == "1 minute":
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
            if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
                return
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
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["config"]
        o = []
        for m in ctx.guild.members:
            if m.status == discord.Status.online:
                o.append(m)
        if table.find_one(key="lvl1_vote_time") is None or table.find_one(key="lvl1_vote_time")["value"] == "1 minute":
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
            if table.find_one(key="muted_role")["value"] == "muted" or table.find_one(key="muted_role") == None:
                role = discord.utils.get(ctx.guild.roles, name="muted")
            else:
                role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
            if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
                return
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
        if ctx.invoked_subcommand == None:
            await ctx.send("you must use a valid subcommand :3")

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

    @room.command(aliases=["delet"])
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

    @commands.group()
    async def config(self, ctx):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        elif ctx.invoked_subcommand is None:
            await ctx.send("```Values you can edit using p!config set:\n\nmuted_role     This changes the muted role. Defaults to \"muted\"\n\nstarboard_channel     Changes what the starboard channel is named. Set to \"off\" to turn starboard off. Defaults to \"off\"\n\nlvl1_vote_time     Changes the vote time for the change nickname, mute, and channel topic Mod Vote commands. Defaults to \"1m\"\n\nlvl2_vote_time     Same thing as lvl1_vote_time, but for kicks and bans. Defaults to \"5m\"\n\nmodlog_channel     The name of the channel that the bot will post modlog messages to. Set to \"off\" to turn the modlog off. Defaults to \"off\"```")

    @config.command()
    async def set(self, ctx, key, value):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
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
            else:
                await ctx.send("Hmm... that's not a valid key!")
                return

    @config.command()
    async def get(self, ctx, key):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
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
            else:
                await ctx.send("Hmm... that's not a valid key!")
                return

    @config.command()
    async def reset(self, ctx, key):
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send("Sorry! You must have the **Manage Server** permission to edit the configuation!")
            return
        else:
            db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
            table = db["config"]
            table.delete(key=key)
            await ctx.send("Config updated!")

    async def on_member_update(self, before, after):
        if before.nick != after.nick:
            db = dataset.connect("sqlite:///{}.db".format(after.guild.id))
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
        db = dataset.connect("sqlite:///{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has joined".format(member.name))
        embed.set_footer(text="User Join", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_remove(self, member):
        db = dataset.connect("sqlite:///{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has left".format(member.name))
        embed.set_footer(text="User Leave", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_ban(self, guild, member):
        db = dataset.connect("sqlite:///{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been banned".format(member.name))
        embed.set_footer(text="User Ban", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    async def on_member_unban(self, guild, member):
        db = dataset.connect("sqlite:///{}.db".format(member.guild.id))
        table = db["config"]
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        channel = discord.utils.get(member.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been unbanned".format(member.name))
        embed.set_footer(text="User Unban", icon_url=member.avatar_url)
        await channel.send(embed=embed)

    @commands.command()
    async def fchangenick(self, ctx, nick, user: discord.Member):
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
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("Sorry! You must have the **Kick Members** permission to use this command!")
            return
        await user.kick()
        await ctx.send("Done!")

    @commands.command()
    async def fban(self, ctx, user: discord.Member):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("Sorry! You must have the **Ban Members** permission to use this command!")
            return
        await user.ban()
        await ctx.send("Done!")

    @commands.command()
    async def fmute(self, ctx, user: discord.Member):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="muted_role")["value"] == "muted" or table.find_one(key="muted_role") == None:
            role = discord.utils.get(ctx.guild.roles, name="muted")
        else:
            role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been muted".format(user.name))
        embed.set_footer(text="User Mute", icon_url=user.avatar_url)
        await mlchannel.send(embed=embed)
        await user.add_roles(role)
        await ctx.send("Done!")

    @commands.command()
    async def funmute(self, ctx, user: discord.Member):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("Sorry! You must have the **Manage Messages** permission to use this command!")
            return
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        table = db["config"]
        if table.find_one(key="muted_role")["value"] == "muted" or table.find_one(key="muted_role") == None:
            role = discord.utils.get(ctx.guild.roles, name="muted")
        else:
            role = discord.utils.get(ctx.guild.roles, name=table.find_one(key="muted_role")["value"])
        if table.find_one(key="modlog_channel") is None or table.find_one(key="modlog_channel")["value"] == "off":
            return
        mlchannel = discord.utils.get(ctx.guild.channels, name=table.find_one(key="modlog_channel")["value"])
        embed = discord.Embed(color=0xffff00, description="User **{}** has been unmuted".format(user.name))
        embed.set_footer(text="User Unmute", icon_url=user.avatar_url)
        await mlchannel.send(embed=embed)
        await user.remove_roles(role)
        await ctx.send("Done!")

def setup(bot):
    bot.add_cog(Moderation(bot))
