import discord
from discord.ext import commands
import asyncio
import random
import aiohttp
import dateutil.parser
import dataset
from urllib.parse import quote_plus

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def broke(self, ctx, *, machine):
        """[machine] broke"""
        embed = discord.Embed(color=0xffff00, description="{} machine broke".format(machine))
        await ctx.send(embed=embed)

    @commands.command()
    async def dice(self, ctx):
        """Rolls a 6-sided dice!"""
        embed = discord.Embed(color=0xffff00, description="Rolling...")
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(1.0)
        embed = discord.Embed(color=0xffff00, description="Rolled a {}!".format(random.randint(1, 6)))
        await msg.edit(embed=embed)

    @commands.command()
    async def joke(self, ctx):
        """Gets a random joke!"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke") as r:
                data = await r.json()
                setup = data["setup"]
                punchline = data["punchline"]
                embed = discord.Embed(title="Joke", description=setup, color=0xffff00)
                embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
                embed.set_footer(text=punchline)
                await ctx.send(embed=embed)

    @commands.command()
    async def chucknorris(self, ctx):
        """Gets a random Chuck Norris fact."""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.chucknorris.io/jokes/random") as r:
                data = r.json()
                fact = data["value"]
                embed = discord.Embed(title="Chuck Norris Fact", description=fact, color=0xffff00)
                embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
                await ctx.send(embed=embed)

    @commands.command()
    async def random(self, ctx, *choices):
        """Picks a random choice"""
        choice = random.choice(choices)
        embed = discord.Embed(color=0xffff00, description="I chose {}!".format(choice))
        await ctx.send(embed=embed)

    @commands.command()
    async def doggo(self, ctx):
        """Shows a random doggo"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                await ctx.send(data["url"])

    @commands.command()
    async def catto(self, ctx):
        """Shows a random catto"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.cat/meow") as r:
                data = await r.json()
                await ctx.send(data["file"])

    @commands.command(aliases=["nsl", "ns"])
    async def nslookup(self, ctx, *, game):
        """Searches for a Nintendo Switch game"""
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("https://api.esho.pw/games") as r:
                    data = await r.json(content_type="text/plain")
                    for g in data:
                        if g["title_lower"] == game.lower():
                            gm = g
                            break
                        else:
                            gm = None
                    if gm is None:
                        await ctx.send("Game not found! Are you sure you spelled it right?")
                        return
                    embed = discord.Embed(color=0xff0000)
                    embed.add_field(name="Title", value=gm["Title"], inline=True)
                    embed.add_field(name="Price", value="${}.{}".format(str(gm["Prices"]["US"])[0:2], str(gm["Prices"]["US"])[-2:]), inline=True)
                    dt = dateutil.parser.parse(gm["Published"])
                    embed.add_field(name="Released", value="{}/{}/{}".format(dt.month, dt.day, dt.year), inline=True)
                    embed.add_field(name="Description", value=gm["Excerpt"], inline=True)
                    embed.add_field(name="Categories", value=", ".join(gm["Categories"]).title(), inline=True)
                    if "metascore" in gm["Metacritic"]:
                        embed.add_field(name="Metacritic Score", value=gm["Metacritic"]["metascore"], inline=True)
                    else:
                        embed.add_field(name="Metacritic Score", value="None found!", inline=True)
                    embed.set_image(url="https://" + gm["Image"][2:])
                    await ctx.send(embed=embed)

    @commands.command()
    async def meme(self, ctx):
        """Pulls a random meme from r/me_irl"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.reddit.com/r/me_irl/random") as r:
                data = await r.json()
                await ctx.send(data[0]["data"]["children"][0]["data"]["url"])

    @commands.command()
    async def greentext(self, ctx):
        """Pulls a random greentext from r/greentext"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.reddit.com/r/greentext/random") as r:
                data = await r.json()
                await ctx.send(data[0]["data"]["children"][0]["data"]["url"])

    @commands.command()
    async def sub(self, ctx, subreddit):
        """Pulls a random post from a subreddit"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.reddit.com/r/{}/random".format(subreddit)) as r:
                data = await r.json()
                if data[0]["data"]["children"][0]["data"]["over_18"] is False:
                    await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
                else:
                    if ctx.channel.is_nsfw() is True:
                        await ctx.send(data[0]["data"]["children"][0]["data"]["url"])
                    else:
                        await ctx.send("https://reddit.com" + data[0]["data"]["children"][0]["data"]["permalink"])

    @commands.command()
    async def wiki(self, ctx, *, page):
        """Searches Wikipedia for a topic"""
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://en.wikipedia.org/w/api.php?action=opensearch&search={}&limit=1&format=json".format(page.lower())) as r:
                data = await r.json()
                if not data[3]:
                    await ctx.send("Sorry, that page doesn't exist!")
                    return
                await ctx.send("Here ya go! " + data[3][0])

    @commands.group(invoke_without_command=True)
    async def quote(self, ctx, *, quote):
        """Retrieves a quote"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        if table.find_one(name=quote):
            await ctx.send(table.find_one(name=quote)["quote"])
        else:
            await ctx.send("Quote not found!")

    @quote.command()
    async def create(self, ctx, name, value):
        """Creates a quote"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        if table.find_one(name=name):
            await ctx.send("Sorry! A quote with that name already exists!")
            return
        table.insert(dict(name=name, quote=value, creator=ctx.author.id))
        await ctx.send("Quote created!")

    @quote.command()
    async def edit(self, ctx, name, value):
        """Edits a quote"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        if table.find_one(name=name):
            if table.find_one(name=name)["creator"] != ctx.author.id:
                await ctx.send("Sorry! Only the creator of the quote can edit it!")
                return
            table.update(dict(name=name, quote=value), ["name"])
            await ctx.send("Quote updated!")

    @quote.command()
    async def creator(self, ctx, *, name):
        """Shows who created a quote"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        if table.find_one(name=name):
            await ctx.send("The person who created ``{}`` is {}".format(name, ctx.guild.get_member(table.find_one(name=name)["creator"]).mention))
        else:
            await ctx.send("Quote not found!")

    @quote.command()
    async def delete(self, ctx, *, name):
        """Deletes a quote"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        if table.find_one(name=name):
            if table.find_one(name=name)["creator"] != ctx.author.id:
                await ctx.send("Sorry! Only the creator of the quote can delete it!")
                return
            table.delete(name=name)
            await ctx.send("Quote deleted!")

    @quote.command()
    async def list(self, ctx):
        """Lists all quotes in this server"""
        db = dataset.connect("sqlite:///servers/{}.db".format(ctx.guild.id))
        table = db["quotes"]
        msg = []
        for q in table.all():
            msg.append(q["name"])
        str = "```{}```".format("\n".join(msg))
        if str == "``````":
            await ctx.send("No quotes found!")
            return
        await ctx.send(str)

    @commands.command()
    async def anime(self, ctx, *, anime):
        """Searches for an anime from MAL"""
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                aurl = quote_plus(anime.lower())
                url = "https://api.jikan.me/search/anime/{}/1".format(aurl)
                async with cs.get(url) as r:
                    resp = await r.json()
                    embed = discord.Embed(color=0xff8c8c, url=resp["result"][0]["url"], title=resp["result"][0]["title"])
                    embed.add_field(name="Description", value=resp["result"][0]["description"], inline=True)
                    embed.add_field(name="Episodes", value=resp["result"][0]["episodes"], inline=True)
                    embed.add_field(name="Rating", value=resp["result"][0]["score"], inline=True)
                    embed.set_image(url=resp["result"][0]["image_url"])
                    await ctx.send(embed=embed)

    @commands.command()
    async def manga(self, ctx, *, manga):
        """Searches for a manga from MAL"""
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                aurl = quote_plus(manga.lower())
                url = "https://api.jikan.me/search/manga/{}/1".format(aurl)
                async with cs.get(url) as r:
                    resp = await r.json()
                    embed = discord.Embed(color=0xff8c8c, url=resp["result"][0]["url"], title=resp["result"][0]["title"])
                    embed.add_field(name="Description", value=resp["result"][0]["description"], inline=True)
                    embed.add_field(name="Volumes", value=resp["result"][0]["volumes"], inline=True)
                    embed.add_field(name="Rating", value=resp["result"][0]["score"], inline=True)
                    embed.set_image(url=resp["result"][0]["image_url"])
                    await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
