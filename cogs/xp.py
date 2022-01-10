import discord
from discord.ext import commands
from level import Data

data = Data()

class xp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # < ----------------------------------------
    #         Check level
    # ---------------------------------------- >
    @commands.command()
    async def level(self, ctx, member: discord.User):
        await data.open_account(member, ctx.guild.id)
        user = await data.get_user_data(member, ctx.guild.id)

        embed = discord.Embed(title=f"{member.name}'s level", color=0xffcff1)
        embed.add_field(name="Level", value=user['level'])
        embed.add_field(name="XP", value=user['xp'])
        await ctx.send(embed=embed, delete_after=15)

    @level.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            user = await data.get_user_data(ctx.author, ctx.guild.id)

            embed = discord.Embed(title=f"{ctx.author.name}'s level", color=0xffcff1)
            embed.add_field(name="Level", value=user['level'])
            embed.add_field(name="XP", value=user['xp'])
            await ctx.send(embed=embed, delete_after=15)

    # < ----------------------------------------
    #         Add guild rank
    # ---------------------------------------- >
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def addrank(self, ctx, role: discord.Role, rank: int):
        await ctx.message.delete()

        error = await data.add_guild_rank(rank, role.id, ctx.guild.id)
        if error:
            embed = discord.Embed(title=f"Couldn't create the reward!", color=0xffcff1)
            embed.add_field(name="Error", value=error)
            await ctx.send(embed=embed, delete_after=15)
        else:
            embed = discord.Embed(title=f"Reward created!", color=0xffcff1)
            embed.add_field(name="Rank", value=str(rank))
            embed.add_field(name="Role", value=role)
            await ctx.send(embed=embed, delete_after=15)
    
    # < ----------------------------------------
    #         Remove guild rank
    # ---------------------------------------- >
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def removerank(self, ctx, level: int):
        await ctx.message.delete()

        error = await data.remove_guild_rank(level, ctx.guild.id)

        if error:
            embed = discord.Embed(title=f"Could not remove reward!", color=0xffcff1)
            embed.add_field(name="Error", value=error)
            await ctx.send(embed=embed, delete_after=15)

        else:
            embed = discord.Embed(title=f"Removed reward!", color=0xffcff1)
            embed.add_field(name="Level", value=str(level))
            await ctx.send(embed=embed, delete_after=15)

    # < ----------------------------------------
    #         View guild ranks
    # ---------------------------------------- >
    @commands.command()
    async def ranks(self, ctx):
        await ctx.message.delete()

        ranks = await data.get_guild_ranks(ctx.guild.id)

        if not ranks:
            embed = discord.Embed(title=f"No reward!", color=0xffcff1)
            embed.add_field(name="There are no ranks!", value="To setup ranks type -addrank @rank level")
            await ctx.send(embed=embed, delete_after=15)
            return

        embed = discord.Embed(title=f"All ranks", color=0xffcff1)
        for r in ranks:
            role = discord.utils.get(ctx.guild.roles, id=int(ranks[r]))
            embed.add_field(name=r, value=role, inline=False)
        await ctx.send(embed=embed, delete_after=15)

def setup(bot):
	bot.add_cog(xp(bot))