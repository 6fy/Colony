from discord.ext import commands
import discord
import random

class duits(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ============()============
    #   Weetjes
    # ============()============

    @commands.command(brief="Returns a cool fact about Germany", aliases=["duitsweetje"])
    async def weetje(self, ctx):
        await ctx.message.delete()

        file = 'assets/data/' + 'weetjes.txt'
        i = 0
        with open(file, 'r', encoding="utf8") as f:
            for line in f.readlines():
                i = i + 1

        rnd = random.randint(0, i-1)
        with open(file, 'r', encoding="utf8") as f:
            weetje = f.readlines()[rnd]

        embed = discord.Embed(title = "Duits weetje", color = 0xfcd112)
        embed.add_field(name = "``Hier is uw weetje``:", value = f'{weetje}', inline = False)

        await ctx.send(embed = embed)

    # ============()============
    #   Foto
    # ============()============

    @commands.command(brief="Returns a cool photo about Germany", aliases=["duitsfotootje", "fotootje"])
    async def foto(self, ctx):
        await ctx.message.delete()

        file = 'assets/data/' + 'fotootjes.txt'
        i = 0
        with open(file, 'r', encoding="utf8") as f:
            for line in f.readlines():
                i = i + 1

        rnd = random.randint(0, i-1)
        with open(file, 'r', encoding="utf8") as f:
            pic = f.readlines()[rnd]

        embed = discord.Embed(title = "Duits fotootje", color = 0xfcd112)
        embed.add_field(name = "``Hier is uw foto``:", value = f'{i}', inline = False)
        embed.set_thumbnail(url = pic)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(duits(bot))