import discord
import dataset

class Starboard:
    def __init__(self, bot):
        self.bot = bot

    async def on_raw_reaction_add(self, emoji, message, channel, user):
        channel = self.bot.get_channel(channel)
        message = await channel.get_message(message)
        db = dataset.connect("sqlite:///{}.db".format(message.guild.id))
        table = db["starboard"]
        config = db["config"]
        if emoji.name == '⭐':
            if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "off":
                return
            if not table.find_one(message=message.id):
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "starboard":
                    channel = discord.utils.get(message.guild.channels, name="starboard")
                else:
                    channel = discord.utils.get(message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                if message.channel == channel:
                    return
                embed = discord.Embed(title="Message by {} starred".format(message.author.name), description="{}".format(message.content), color=0xffff00)
                embed.set_footer(text="This message has received 1 ⭐")
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                msg = await channel.send(embed=embed)
                table.insert(dict(message=message.id, stars=1, starmessage=msg.id))
            else:
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "starboard":
                    channel = discord.utils.get(message.guild.channels, name="starboard")
                else:
                    channel = discord.utils.get(message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                data = table.find_one(message=message.id)
                stars = data["stars"] + 1
                table.update(dict(message=message.id, stars=stars), ["message"])
                data = table.find_one(message=message.id)
                msg = discord.utils.get(await channel.history().flatten(), id=data["starmessage"])
                embed = discord.Embed(title="Message by {} starred".format(message.author.name), description="{}".format(message.content), color=0xffff00)
                embed.set_footer(text="This message has received {} ⭐'s".format(data["stars"]))
                if message.attachments:
                    embed.set_image(url=message.attachments[0].url)
                await msg.edit(embed=embed)

    async def on_raw_reaction_remove(self, emoji, message, channel, user):
        channel = self.bot.get_channel(channel)
        message = await channel.get_message(message)
        db = dataset.connect("sqlite:///{}.db".format(message.guild.id))
        table = db["starboard"]
        config = db["config"]
        if emoji.name == '⭐':
            if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "off":
                return
            if table.find_one(message=message.id):
                data = table.find_one(message=message.id)
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "starboard":
                    channel = discord.utils.get(message.guild.channels, name="starboard")
                else:
                    channel = discord.utils.get(message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                msg = discord.utils.get(await channel.history().flatten(), id=data["starmessage"])
                stars = data["stars"] - 1
                if stars == 0:
                    await msg.delete()
                    table.delete(message=message.id)
                    return
                table.update(dict(message=message.id, stars=stars), ["message"])
                data = table.find_one(message=message.id)
                if stars == 1:
                    embed = discord.Embed(title="Message by {} starred".format(message.author.name), description="{}".format(message.content), color=0xffff00)
                    embed.set_footer(text="This message has received 1 ⭐")
                    if message.attachments:
                        embed.set_image(url=message.attachments[0].url)
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title="Message by {} starred".format(message.author.name), description="{}".format(message.content), color=0xffff00)
                    embed.set_footer(text="This message has received {} ⭐'s".format(data["stars"]))
                    if message.attachments:
                        embed.set_image(url=message.attachments[0].url)
                    await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Starboard(bot))
