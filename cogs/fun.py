import discord
from discord.ext import commands
import pokebase as pb
import asyncio
import random
import requests
from pyshorteners import Shortener
import ast

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pokesearch(self, ctx, pokemon):
        """Searches for a Pokemon using PokeAPI"""
        async with ctx.channel.typing():
            # inside jokes from ember
            if pokemon.lower() == "c0ber":
                await ctx.send(file=discord.File("pokemon/oofasd.png"))
                return
            elif pokemon.lower() == "metoothanks":
                await ctx.send(file=discord.File("pokemon/uhhmetoothanks.png"))
                return
            elif pokemon.lower() == "2hats":
                await ctx.send(file=discord.File("pokemon/faw.png"))
                return
            elif pokemon.lower() == "tj":
                await ctx.send(file=discord.File("pokemon/tj.png"))
                return

            try:
                pkmn = pb.pokemon(pokemon.lower())
            except:
                embed = discord.Embed(color=0xffff00, description="Pokemon not found! Check your spelling and try again!")
                await ctx.send(embed=embed)
                return
            embed = discord.Embed(title=pkmn.name.title(), color=0xffff00)
            embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
            embed.set_thumbnail(url=pkmn.sprites.front_default)
            embed.add_field(name="ID", value=pkmn.id, inline=True)
            embed.add_field(name="Height", value=pkmn.height, inline=True)
            embed.add_field(name="Weight", value=pkmn.weight, inline=True)
            embed.add_field(name="Type", value=pkmn.types[0].type.name.title(), inline=True)
            await ctx.send(embed=embed)

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
        resp = requests.get("https://08ad1pao69.execute-api.us-east-1.amazonaws.com/dev/random_joke")
        data = resp.json()
        setup = data["setup"]
        punchline = data["punchline"]
        embed = discord.Embed(title="Joke", description=setup, color=0xffff00)
        embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
        embed.set_footer(text=punchline)
        await ctx.send(embed=embed)

    @commands.command()
    async def chucknorris(self, ctx):
        """Gets a random Chuck Norris fact."""
        resp = requests.get("https://api.chucknorris.io/jokes/random")
        data = resp.json()
        fact = data["value"]
        embed = discord.Embed(title="Chuck Norris Fact", description=fact, color=0xffff00)
        embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def shorten(self, ctx, url):
        """Shortens a URL"""
        shortener = Shortener("Tinyurl")
        link = shortener.short(url)
        embed = discord.Embed(title="URL Shortened!", url=link, description ="(right click and select \"Copy Link\")", color = 0xffff00)
        embed.set_author(name="Pika.py", icon_url="https://img00.deviantart.net/172c/i/2013/188/f/8/robot_pikachu_by_spice5400-d6ceutv.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def random(self, ctx, *choices):
        choice = random.choice(choices)
        embed = discord.Embed(color=0xffff00, description="I chose {}!".format(choice))
        await ctx.send(embed=embed)

    @commands.command()
    async def doggo(self, ctx):
        resp = requests.get("https://random.dog/woof.json")
        data = resp.json()
        await ctx.send(data["url"])

    @commands.command()
    async def avatar(self, ctx, user: discord.Member):
        await ctx.send(user.avatar_url)

def setup(bot):
    bot.add_cog(Fun(bot))
