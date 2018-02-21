import discord
from discord.ext import commands
import dataset

class Internal:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def rmt(self, ctx):
        menu = await ctx.send("beep boop react")
        await menu.add_reaction('👍')
        await menu.add_reaction('👎')
        await menu.add_reaction('🛑')
        def check(choice, user):
            return user == ctx.author and choice.message.id == menu.id
        while True:
            choice, user = await self.bot.wait_for("reaction_add", check=check)
            print("reaction event triggered")
            if str(choice.emoji) == '👍':
                await menu.edit(content="thanks bro")
                break
            elif str(choice.emoji) == '👎':
                await menu.edit(content=":sob: try again")
                await menu.remove_reaction('👎', user)
            elif str(choice.emoji) == '🛑':
                await menu.edit(content="bye boi")
                break

    @commands.command()
    @commands.is_owner()
    async def ls(self, ctx):
        for g in self.bot.guilds:
            await ctx.send("{}: {}".format(g.name, str(await g.channels[0].create_invite(unique=False))))

    @commands.command()
    @commands.is_owner()
    async def csb(self, ctx):
        db = dataset.connect("sqlite:///{}.db".format(ctx.guild.id))
        for r in db["starboard"]:
            db["starboard"].delete(message=r["message"])
        await ctx.send("done? starboard db *should* be cleared...")

    @commands.command()
    @commands.is_owner()
    async def startest(self, ctx):
        m = await ctx.send("test dont star")
        await m.add_reaction('⭐')

def setup(bot):
    bot.add_cog(Internal(bot))
