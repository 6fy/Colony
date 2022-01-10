import discord, subprocess, sys, time
from discord.ext import commands

class dev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # < ----------------------------------------
    #         Reload
    # ---------------------------------------- > 

    @commands.command(aliases=['r', 'reload', 'rl'], brief='Reloads a file')
    @commands.is_owner()
    async def update(self, ctx, cog):
        await ctx.message.delete()
        
        message = await ctx.send(f"<a:load:927511196133908480>> Restarting Cog ➜ `{cog}`...")
        self.bot.unload_extension(f"cogs.{cog}")
        self.bot.load_extension(f"cogs.{cog}")

        print(f"Updated ➜ {cog}")
        await message.edit(content=f"<:verify:927511181919395841> Restarted Cog ➜ `{cog}`!", delete_after=5)
    
    @update.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.message.delete()
            await ctx.send("You are not the bot creator, you cannot execute this command!", delete_after=5)
        if isinstance(error, commands.ExtensionNotFound):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)
        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.message.delete()
            await ctx.send("That cog is not loaded!", delete_after=5)

    # < ----------------------------------------
    #         Cogs
    # ---------------------------------------- > 

    @commands.command(aliases=['cog'], brief='Looks for loaded/unloaded cogs')
    @commands.is_owner()
    async def cogs(self, ctx):
        await ctx.message.delete()

        cogsList = ""
        for cog in self.bot.cogs: 
            meow = f"cogs.{cog}"
            try:
                self.bot.load_extension(meow)
            except commands.ExtensionAlreadyLoaded:
                cogsList += f"→ {cog} is loaded \n"
            except commands.ExtensionNotFound:
                cogsList += f"↓ {cog} is not found \n"
            else:
                cogsList += f"← {cog} not loaded \n"

        await ctx.send(f"```{cogsList}```", delete_after=15)

    # < ----------------------------------------
    #         Custom Help Command
    # ---------------------------------------- > 

    @commands.command(aliases=['clearconsole'], brief='Clears console')
    @commands.is_owner()
    async def log(self, ctx):
        await ctx.message.delete()

        x = 1
        while x < 10:
            print("\n")
            x = x + 1 
 
    # < ----------------------------------------
    #         Load
    # ---------------------------------------- > 

    @commands.command(aliases=['enable', 'l'], brief='Loads a file')
    @commands.is_owner()
    async def load(self, ctx, cog):
        await ctx.message.delete()
        message = await ctx.send(f"<a:load:927511196133908480>> Loading Cog ➜ `{cog}`...")
        self.bot.load_extension(f"cogs.{cog}")

        print(f"Loaded ➜ {cog}")
        await message.edit(content=f"<:verify:927511181919395841> Loaded Cog ➜ `{cog}`!", delete_after=5)

    @load.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.message.delete()
            await ctx.send("You are not the bot creator, you cannot execute this command!", delete_after=5)
        if isinstance(error, commands.CommandInvokeError):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)
        if isinstance(error, commands.ExtensionNotFound):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)
        if isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)

    # < ----------------------------------------
    #         unload
    # ---------------------------------------- > 

    @commands.command(aliases=['disable', 'd'], brief='Unloads a file')
    @commands.is_owner()
    async def unload(self, ctx, cog):
        await ctx.message.delete()
        if cog == "dev":
            return await ctx.send("<a:load:927511196133908480>> You cannot unload dev!", delete_after=5)
        message = await ctx.send(f"<a:load:927511196133908480>> Unloading Cog ➜ `{cog}`...")
        self.bot.unload_extension(f"cogs.{cog}")
        print(f"Unloaded ➜ {cog}")
        await message.edit(content=f"<:verify:927511181919395841> Unloaded Cog ➜ `{cog}`!", delete_after=5)

    @unload.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)
        if isinstance(error, commands.ExtensionNotLoaded):
            await ctx.message.delete()
            await ctx.send("That cog is not loaded!", delete_after=5)
        if isinstance(error, commands.NotOwner):
            await ctx.message.delete()
            await ctx.send("You are not the bot creator, you cannot execute this command!", delete_after=5)
        if isinstance(error, commands.ExtensionNotFound):
            await ctx.message.delete()
            await ctx.send("I could not find that cog!", delete_after=5)

    # < ----------------------------------------
    #         Restart
    # ---------------------------------------- > 

    @commands.command(brief='Restarts the bot')
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"<a:load:927511196133908480> ➜ The bot is restarting and will be online soon!") 
        await self.bot.close()
        subprocess.call([sys.executable, "main.py"])

def setup(bot):
    bot.add_cog(dev(bot))