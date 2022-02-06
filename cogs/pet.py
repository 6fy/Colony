import discord
import random
import asyncio

from discord.ext import commands

try:
    from assets.imports.pet import Pet
    pet = Pet()

except ModuleNotFoundError:
    print('ModuleNotFoundError: Did you run main.py?')

class pets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pets = ["cat", "dog", "giraffe"]

    # ============()============
    #    Adopt a pet
    # ============()============

    @commands.command(brief="Adopt a pet")
    async def adopt(self, ctx):
        await ctx.message.delete()

        users = await pet.get_users()
        if str(ctx.author.id) in users:
            type_pet = users[str(ctx.author.id)]['pet']
            embed = discord.Embed(title=f"Could not adopt a pet", color=0xfff)
            embed.add_field(name="``Forbidden``", value=f'It seems like you already own a {type_pet}')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        owner = await pet.update_account(ctx.author, {"pet": random.choice(self.pets), "pet_level": 0, "pet_xp": 0})
        type_pet = owner['pet']

        embed = discord.Embed(title=f"{ctx.author} received a pet", color=0xfff)
        embed.add_field(name=f"``New pet``", value=f'Enjoy your new {type_pet}')
        await ctx.channel.send(embed=embed, delete_after=10)

    # ============()============
    #    View your pets stats
    # ============()============

    @commands.command(brief="Adopt a pet")
    async def pet(self, ctx, member: discord.User = None):
        await ctx.message.delete()

        users = await pet.get_users()

        player = ctx.author
        if member != None:
            player = member

        if str(player.id) not in users:
            embed = discord.Embed(title=f"Could not view pet", color=0xfff)
            embed.add_field(name="``Forbidden``", value=f'It seems like you don\'t own a pet')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        stats = users[str(player.id)]

        embed = discord.Embed(title=f"{player.name}'s pet", color=0xfff)
        embed.add_field(name="``Type``", value=stats['pet'])
        embed.add_field(name="``Level``", value=stats['pet_level'])
        embed.add_field(name="``Experience``", value=stats['pet_xp'])
        await ctx.channel.send(embed=embed, delete_after=30)        

    # ============()============
    #    Fight a players pet
    # ============()============

    @commands.command(brief="Fight a players pet", aliases=["duel", "fighr"])
    @commands.cooldown(1, 300, commands.BucketType.user) # Commands available every 5 minutes
    async def fight(self, ctx, dueled: discord.User = None):
        await ctx.message.delete()

        if dueled == ctx.author:
            return

        # No user given
        if dueled == None:
            embed = discord.Embed(title=f"Could not fight this player", color=0xfff)
            embed.add_field(name="``Invalid argument``", value=f'Try /fight player')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        users = await pet.get_users()

        # User doesn't have a pet 
        if str(ctx.author.id) not in users:
            embed = discord.Embed(title=f"Could not fight this player", color=0xfff)
            embed.add_field(name="``Forbidden``", value=f'It seems like you don\'t own a pet')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        # Other user doesn't have a pet 
        if str(dueled.id) not in users:
            embed = discord.Embed(title=f"Could not fight this player", color=0xfff)
            embed.add_field(name="``Forbidden``", value=f'It seems like they don\'t own a pet')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

        # Setting up a message
        accept = '✅'
        deny = '❌'

        msg = await ctx.send(f'<@{dueled.id}>, {ctx.author.name} Wishes to fight your pet! Do you accept their duel?', delete_after=30)
        await msg.add_reaction(accept)
        # await msg.add_reaction(deny)

        # Checking if the challenged user accepted
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=lambda reaction, user: user == dueled and reaction.emoji in [accept, deny], timeout=30.0)

        except asyncio.TimeoutError:
            # User didn't accept in time
            embed = discord.Embed(title=f"{ctx.author.name}\'s fight request to {dueled.name} expired", color=0xfff)
            embed.add_field(name="``Fight denied``", value=f'{dueled.name} didn\'t respond in time')
            await ctx.channel.send(embed=embed, delete_after=5)
            return

        if reaction.emoji == accept:
            await set_battle(ctx, ctx.author, dueled, 9 + users[str(ctx.author.id)]['pet_level'], 9 + users[str(dueled.id)]['pet_level'], users)

def setup(bot):
    bot.add_cog(pets(bot))

async def set_battle(ctx, author: discord.User, dueled: discord.User, duelerHealth, accepterHealth, users):
    pick = random.randint(0, 1)
    hit = random.randint(1, 8)

    # The dueler is going to get hit
    if pick == 0:
        duelerHealth -= hit
        if duelerHealth < 0:
            duelerHealth = 0

        maxHealth = 9 + users[str(author.id)]['pet_level']

        embed = discord.Embed(title=f"{dueled.name}'s pet hit {author.name}'s pet for {hit}", color=0xf50add)
        embed.add_field(name="``Hit landed!``", value=f'**{author.name}**\'s pet health is: **{duelerHealth}/{maxHealth}**')
        await ctx.channel.send(embed=embed, delete_after=30)

    # The accepter is going to get hit
    else:
        accepterHealth -= hit
        if accepterHealth < 0:
            accepterHealth = 0

        maxHealth = 9 + users[str(dueled.id)]['pet_level']

        embed = discord.Embed(title=f"{author.name}'s pet hit {dueled.name}'s pet for {hit}", color=0xf4fc08)
        embed.add_field(name="``Hit landed!``", value=f'**{dueled.name}**\'s pet health is: **{accepterHealth}/{maxHealth}**')
        await ctx.channel.send(embed=embed, delete_after=30)

    if duelerHealth == 0 or accepterHealth == 0:
        # The dueler won
        if duelerHealth > 0:
            await pet.update_account(ctx.author, {"pet": users[str(ctx.author.id)]['pet'], "pet_level": 0, "pet_xp": 10})
            maxHealth = 9 + users[str(ctx.author.id)]['pet_level']

            embed = discord.Embed(title=f"{ctx.author.name}'s pet won the fight!", color=0xf50add)
            embed.add_field(name="``Fight won``", value=f'{ctx.author.name}\'s pet has {duelerHealth}/{maxHealth} HP left')
            await ctx.channel.send(embed=embed, delete_after=30)

            await ctx.channel.send(f'{ctx.author.name}\'s pet has gotten 10 experience points!', delete_after=5)

        # The accepter won
        else:
            await pet.update_account(dueled, {"pet": users[str(dueled.id)]['pet'], "pet_level": 0, "pet_xp": 10})
            maxHealth = 9 + users[str(dueled.id)]['pet_level']

            embed = discord.Embed(title=f"{dueled.name}'s pet won the fight!", color=0xf4fc08)
            embed.add_field(name="``Fight won``", value=f'{dueled.name}\'s pet has {accepterHealth}/{maxHealth} HP left')
            await ctx.channel.send(embed=embed, delete_after=30)

            await ctx.channel.send(f'{dueled.name}\'s pet has gotten 10 experience points!', delete_after=5)

    else:
        await set_battle(ctx, author, dueled, duelerHealth, accepterHealth, users)
