import discord
import dataset

class Starboard:
    def __init__(self, bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(reaction.message.guild.id))
        table = db["starboard"]
        config = db["config"]
        if reaction.emoji == '⭐':
            if not table.find_one(message=reaction.message.id):
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "off":
                    return
                channel = discord.utils.get(reaction.message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                if reaction.message.channel == channel:
                    return
                embed = discord.Embed(title="Message by {} starred".format(reaction.message.author.name), description="{}".format(reaction.message.content), color=0xffff00)
                embed.set_footer(text="This message has received 1 ⭐")
                if reaction.message.attachments:
                    embed.set_image(url=reaction.message.attachments[0].url)
                msg = await channel.send(embed=embed)
                table.insert(dict(message=reaction.message.id, stars=1, starmessage=msg.id))
            else:
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "starboard":
                    channel = discord.utils.get(reaction.message.guild.channels, name="starboard")
                else:
                    channel = discord.utils.get(reaction.message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                data = table.find_one(message=reaction.message.id)
                stars = data["stars"] + 1
                table.update(dict(message=reaction.message.id, stars=stars), ["message"])
                data = table.find_one(message=reaction.message.id)
                msg = discord.utils.get(await channel.history().flatten(), id=data["starmessage"])
                embed = discord.Embed(title="Message by {} starred".format(reaction.message.author.name), description="{}".format(reaction.message.content), color=0xffff00)
                embed.set_footer(text="This message has received {} ⭐'s".format(data["stars"]))
                if reaction.message.attachments:
                    embed.set_image(url=reaction.message.attachments[0].url)
                await msg.edit(embed=embed)

    async def on_reaction_remove(self, reaction, member):
        db = dataset.connect("sqlite:///servers/{}.db".format(reaction.message.guild.id))
        table = db["starboard"]
        config = db["config"]
        if reaction.emoji == '⭐':
            if table.find_one(message=reaction.message.id):
                data = table.find_one(message=reaction.message.id)
                if config.find_one(key="starboard_channel") is None or config.find_one(key="starboard_channel")["value"] == "off":
                    return
                channel = discord.utils.get(reaction.message.guild.channels, name=config.find_one(key="starboard_channel")["value"])
                msg = discord.utils.get(await channel.history().flatten(), id=data["starmessage"])
                stars = data["stars"] - 1
                if stars == 0:
                    await msg.delete()
                    table.delete(message=reaction.message.id)
                    return
                table.update(dict(message=reaction.message.id, stars=stars), ["message"])
                data = table.find_one(message=reaction.message.id)
                if stars == 1:
                    embed = discord.Embed(title="Message by {} starred".format(reaction.message.author.name), description="{}".format(reaction.message.content), color=0xffff00)
                    embed.set_footer(text="This message has received 1 ⭐")
                    if reaction.message.attachments:
                        embed.set_image(url=reaction.message.attachments[0].url)
                    await msg.edit(embed=embed)
                else:
                    embed = discord.Embed(title="Message by {} starred".format(reaction.message.author.name), description="{}".format(reaction.message.content), color=0xffff00)
                    embed.set_footer(text="This message has received {} ⭐'s".format(data["stars"]))
                    if reaction.message.attachments:
                        embed.set_image(url=reaction.message.attachments[0].url)
                    await msg.edit(embed=embed)

def setup(bot):
    bot.add_cog(Starboard(bot))
