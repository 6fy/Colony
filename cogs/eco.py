from discord.enums import UserFlags
from discord.ext import commands
from economy import Balance

bal = Balance()

import discord

class eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ============()============
    #   Check your balance
    # ============()============

    @commands.command(brief="Check how much money you have", aliases=["money", "bal"])
    async def balance(self, ctx):
        await ctx.message.delete()

        await bal.create_account(ctx.author, ctx.guild.id)
        users = await bal.get_all_users()

        if str(ctx.author.id) in users[str(ctx.guild.id)]:
            balance = users[str(ctx.guild.id)][str(ctx.author.id)]["balance"]

        embed = discord.Embed(title = "Duits geld", color = 0xfcd112)
        embed.add_field(name = f"``Hier is uw geld {ctx.author.name}``:", value = balance, inline = False)
        await ctx.send(embed = embed)


    # await bal.update_balance(ctx.author, 100, ctx.guild.id)

def setup(bot):
    bot.add_cog(eco(bot))