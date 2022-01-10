import discord
import random

from discord.ext import commands

from economy import Balance
bal = Balance()

from convert import Converter
convert = Converter()

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
            job = f':police_car: You worked as a police agent today and earned ¥{daily} Yen!'
        else:
            job = f':airplane: You worked as a pilot today and earned ¥{daily} Yen!'

        await bal.update_balance(ctx.author, daily, ctx.guild.id)

        embed = discord.Embed(title=f"{ctx.author.name}'s daily report!", color=0xfff)
        embed.add_field(name="``Work report:``", value=job, inline = False)
        await ctx.send(embed=embed)

    @daily.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            secs = int(error.retry_after)
            msg = f'**Cooldown**, please try again in {secs} seconds'
            await ctx.send(msg, delete_after=5)

    # ============()============
    #    Leaderboards 
    # ============()============

    @commands.command(brief="Find out who the riches person is", aliases = ["lb", "lbs"])
    async def leaderboard(self, ctx, x = 11):
        users = await bal.get_guild_users(ctx.guild.id)

        total = []
        members = []
        for id in users:
            total_amount = users[str(id)]["balance"]
            total.append(total_amount)
            members.append(id)

        sort = sorted(total, reverse=True)

        max = 5
        for v in range(len(sort)):
            if v > max:
                total.pop(v)
                members.pop(v)
        
        embed = discord.Embed(title=f":money_with_wings: Top {max} Richest People", description="View the people with the most amount of money", color=0xfff)

        for i in range(len(total)):
            member = await self.bot.fetch_user(members[i])
            embed.add_field(name = f"{i+1}. {member}" , value = f"**¥{total[i]}** Yen",  inline = False)

        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(eco(bot))