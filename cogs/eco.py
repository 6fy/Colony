import discord
import random
import asyncio

from discord.ext import commands

try:
    from assets.imports.economy import Balance
    bal = Balance()

    from assets.imports.convert import Converter
    convert = Converter()

    from assets.imports.questions import Questions
    q = Questions()
    questions = q.questions

except ModuleNotFoundError:
    print('ModuleNotFoundError: Did you run main.py?')

class eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ============()============
    #   Check your balance
    # ============()============

    @commands.command(brief="Check how much money you have", aliases=["money", "bal"])
    async def balance(self, ctx, member: discord.Member = None):
        await ctx.message.delete()

        if member == None:
            member = ctx.author

        await bal.create_account(member, ctx.guild.id)
        users = await bal.get_all_users()

        if str(member.id) in users[str(ctx.guild.id)]:
            balance = users[str(ctx.guild.id)][str(member.id)]["balance"]

        embed = discord.Embed(title = f"{member.name}'s balance", color = 0xfff)
        embed.add_field(name = f"``Balance:``", value = f'¥{balance} Yen', inline = False)
        await ctx.send(embed = embed)

    # ============()============
    #   Get money daily
    # ============()============
    @commands.command(brief="Get money daily", aliases=["work"])
    @commands.cooldown(1, 86400, commands.BucketType.user) # Commands available every 24 hours
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

    # ============()============
    #    Leaderboards 
    # ============()============

    @commands.command(brief="Find out who the riches person is", aliases = ["lb", "lbs"])
    async def leaderboard(self, ctx, total: int = None):
        users = await bal.get_guild_users(ctx.guild.id)

        total = [] # Total amount to sort it
        members = [] # Members to print out the members later
        # Looping through all the users and adding them to the lists
        for id in users:
            total_amount = users[str(id)]["balance"]
            total.append(total_amount)
            members.append(id)

        # Sorting the total (amount) list 
        sort = sorted(total, reverse=True)

        # Get 5 highest values
        max = 5
        if total is not None:
            max = int(total)

        for v in range(len(sort)):
            # If the value is lower than the 5th place remove them
            if v > max:
                total.pop(v)
                members.pop(v)
        
        embed = discord.Embed(title=f":money_with_wings: Top {max} Richest People", description="View the people with the most amount of money", color=0xfff)

        for i in range(len(total)):
            member = await self.bot.fetch_user(members[i])
            embed.add_field(name = f"{i+1}. {member}" , value = f"**¥{total[i]}** Yen",  inline = False)

        await ctx.send(embed = embed)

    # ============()============
    #    Gamble your money 
    # ============()============

    @commands.command(brief="Gamble your money", aliases = ["bet"])
    async def gamble(self, ctx, bet: str = None):
        await ctx.message.delete()

        users = await bal.get_guild_users(ctx.guild.id)
        balance = users[str(ctx.author.id)]['balance']

        if bet is None:
            embed = discord.Embed(title=f"You are missing a required argument!", color=0xfff)
            embed.add_field(name="``Example: ?bet 3``", value="Please enter an amount you want to bet.", inline = False)
            await ctx.send(embed=embed, delete_after=5)
            return

        if bet == "all":
            bet = balance
        else:
            bet = int(bet)

        await bal.update_balance(ctx.author, -bet, ctx.guild.id)

        # user does not have enough money
        if balance < bet: 
            embed = discord.Embed(title=f"You cannot afford this bet!", color=0xfff)
            embed.add_field(name="``Example: ?bet 3``", value="Please lower the amount you want to bet to afford this option.", inline = False)
            await ctx.send(embed=embed, delete_after=5)
            return
        
        # amount is not positive
        if bet <= 0:
            embed = discord.Embed(title=f"This is an invalid amount!", color=0xfff)
            embed.add_field(name="``Example: ?bet 3``", value="Please higher the amount you want to bet to execute this option.", inline = False)
            await ctx.send(embed=embed, delete_after=5)
            return

        slots = []
        for i in range(3):
            slots.append(random.choice(['Apple', 'Cherry', 'Banana']))
        
        # Jackpot
        if slots[0] is slots[1] and slots[1] is slots[2]:
            embed = discord.Embed(title=f":money_with_wings: {ctx.author.name}'s slot machine prize (¥{bet})", color=0xfff)
            embed.add_field(name=f"``Jackpot``", value=f"¥{bet * 5} Yen has been added to your account!", inline = False)
            await ctx.send(embed=embed)
            prize = bet * 5

        # Won
        elif slots[0] is slots[1] or slots[0] is slots[2] or slots[0] is slots[2]:
            embed = discord.Embed(title=f":money_with_wings: {ctx.author.name}'s slot machine prize (¥{bet})", color=0xfff)
            embed.add_field(name=f"``Won``", value=f"¥{bet * 2} Yen has been added to your account!", inline = False)
            await ctx.send(embed=embed)
            prize = bet * 2

        # Lost
        else:
            embed = discord.Embed(title=f":money_with_wings: {ctx.author.name}'s slot machine prize (¥{bet})", color=0xfff)
            embed.add_field(name=f"``Lost``", value=f"You've lost the gamble", inline = False)
            await ctx.send(embed=embed)
            prize = 0

        await bal.update_balance(ctx.author, prize, ctx.guild.id)

    # ============()============
    #    Answer a question for money
    # ============()============

    @commands.command(brief="Answer a question for money")
    async def quiz(self, ctx, bet: int = None):
        await ctx.message.delete()

        users = await bal.get_guild_users(ctx.guild.id)
        balance = users[str(ctx.author.id)]['balance']

        if bet is None:
            bet = 50
        
        if bet <= 0:
            bet = 50

        if bet == "all":
            bet = balance
        else:
            bet = int(bet)

        if balance < bet:
            embed = discord.Embed(title="Not enough money!", color=0xfff)
            embed.add_field(name=f"You need at least ¥50 Yen to play this, or define a bet", value=f"Example: ?quiz 5", inline = False)
            await ctx.send(embed=embed)
            return

        correct = '✅'
        false = '❌'

        chosen_question = random.randint(0, len(questions) - 1)
        question = questions[chosen_question]

        msg = await ctx.send(question["text"], delete_after=30)
        await msg.add_reaction(correct)
        await msg.add_reaction(false)

        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == ctx.author and reaction.emoji in [correct, false], timeout=30.0)

        except asyncio.TimeoutError:
            await ctx.send('Question time expired', delete_after=5)
            return
        
        answered = True if question["answer"] == True else False

        if reaction.emoji == correct:
            await send_message(ctx, answered, question["explaination"], bet)
        
        elif reaction.emoji == false:
            await send_message(ctx, not answered, question["explaination"], bet)

def setup(bot):
    bot.add_cog(eco(bot))

async def send_message(ctx, correct: bool, explaination: str, bet: int):
    if correct:
        title = f'Wow you\'re smart. Your reward is ¥{bet} Yen!'
        color = 0x0af531
        await bal.update_balance(ctx.author, bet, ctx.guild.id)

    else:
        title = f'You\'re talented in the head if you think you\'re correct. You lost ¥{bet} Yen!'
        color = 0xf50f26
        await bal.update_balance(ctx.author, -bet, ctx.guild.id)

    embed = discord.Embed(title=title, color=color)
    embed.add_field(name=f"Correctly answered: {correct}", value=f"Explaination: {explaination}", inline = False)
    await ctx.send(embed=embed)