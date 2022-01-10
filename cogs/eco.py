import discord
import random

from discord.ext import commands

from economy import Balance
bal = Balance()

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

        embed = discord.Embed(title = f"{ctx.author.name}'s balance", color = 0xfff)
        embed.add_field(name = f"``Balance:``", value = balance, inline = False)
        await ctx.send(embed = embed)

    # ============()============
    #   Get money daily
    # ============()============
    @commands.command(brief="Get money daily", aliases=["work"])
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        await ctx.message.delete()
    
        await bal.create_account(ctx.author, ctx.guild.id)

        daily = random.randint(1, 25)

        if daily <= 5:
            job = f':taxi: You worked as a taxi driver today and earned ¥{daily} Yen!'
        elif daily > 5 and daily <= 15:
            job = f':police_car: You worked as a police agent driver today and earned ¥{daily} Yen!'
        else:
            job = f':airplane: You worked as a pilot today and earned ¥{daily} Yen!'

        await bal.update_balance(ctx.author, daily, ctx.guild.id)

        embed = discord.Embed(title=f"{ctx.author.name}'s daily report!", color=0xfff)
        embed.add_field(name="``Work report:``", value=job, inline = False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(eco(bot))