import discord
import random

from discord.ext import commands
from discord.ext.commands import CommandNotFound

from assets.imports.level import Data
data = Data()

from assets.imports.convert import Converter
convert = Converter()

# < ----------------------------------------
#         Bot variables
# ---------------------------------------- >

with open('assets/bot/configuration/' + 'config.0', 'r') as f:
    lines = f.readlines()
    token = lines[0]
    prefix = lines[1]

client = commands.Bot(command_prefix=prefix)

# < ----------------------------------------
#         Client events
# ---------------------------------------- >

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="? commands"))
    print(f"{client.user} has launched!")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(title=f"An error occurred!", color=0xfff)
        embed.add_field(name="``CommandNotFound``", value=f'There is no command found called **{ctx.message.content}**')
        await ctx.channel.send(embed=embed, delete_after=10)
        return
    
    if isinstance(error, commands.CommandOnCooldown):
        secs = await convert.secondsToTimeText(int(error.retry_after))

        embed = discord.Embed(title=f"You are currently on a cooldown!", color=0xfff)
        embed.add_field(name="**Cooldown**", value=f'You can execute this command again in {secs}')
        await ctx.channel.send(embed=embed, delete_after=10)
        return

    if isinstance(error, ValueError):
        embed = discord.Embed(title=f"An error occurred!", color=0xfff)
        embed.add_field(name="``ValueError``", value=f'Please make sure your argument is a number')
        await ctx.channel.send(embed=embed, delete_after=10)
        return
    
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title=f"An error occurred!", color=0xfff)
        embed.add_field(name="``BadArgument``", value=f'Please make sure your argument is a number')
        await ctx.channel.send(embed=embed, delete_after=10)
        return

    raise error

@client.event
async def on_message(ctx):
    xp = random.randint(1, 3)
    await data.open_account(ctx.author, ctx.guild.id)
    await data.update_user(ctx.guild.id, ctx.author, xp)

    role_id = await data.get_user_rank(ctx.author, ctx.guild.id)
    if role_id:
        try:
            r = discord.utils.get(ctx.guild.roles, id=int(role_id))
            await ctx.author.add_roles(r)
        except discord.errors.Forbidden:
            embed = discord.Embed(title=f"I couldn't apply the role!", color=0xfff)
            embed.add_field(name="``Forbidden``", value='Make sure I have "manage_roles" permissions and my role is above the role you are trying to apply!')
            await ctx.channel.send(embed=embed, delete_after=10)
            return
        except ValueError:
            embed = discord.Embed(title=f"I couldn't apply the role!", color=0xfff)
            embed.add_field(name="``ValueError``", value=f'The role with the id {role_id} is not found!')
            await ctx.channel.send(embed=embed, delete_after=10)
            return

    try:
        await client.process_commands(ctx)
    except:
        pass

# < ----------------------------------------
#         Loading the bot
# ---------------------------------------- >

cogs = {
    'cogs.eco',
    'cogs.dev',
    'cogs.xp',
}

if __name__ == "__main__":
    for cog in cogs:
        client.load_extension(cog)
        print(f"{cog} has been loaded")

client.run(token, bot=True)