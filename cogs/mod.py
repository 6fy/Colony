from discord.ext import commands

class mod(commands.Cog): # making a class with the cog as parameter
  def __init__(self, bot): # this will initialize when the class is called
    self.bot = bot

  @commands.command(brief="Kick a user from the guild", aliases=["remove", "delete"]) # register a command with brief as description and aliases as extra naming for the same command
  async def kick(self, ctx, user): # called the function and the name is the command so -kick in this example
  # self and ctx are mendatory, user is optional
    await ctx.message.delete() # this deletes the message (-kick ... in this example)

    if user == None: # check if -kick >> .... << is none 
      await ctx.send("Please specify a user")
      return

    await ctx.send(f"Pretty mean of you to want to kick {user}") # sending a message
  
  # @kick.error # this will execute if there's an error
  # async def on_command_error(self, ctx, error): # all necessary
  #   if isinstance(error, commands.MissingRequiredArgument): # this checks for the error with the error class MissingRequiredArgument you don't have to put this if statement but i suggest you do to make it easier to troubleshoot and nicer for the ux (user experience)
  #     await ctx.message.delete()
  #     await ctx.send("Please specify a user", delete_after=10) # delete_after will delete the message after x seconds if you don't wanna delete it you just remove the part after the string so just put ctx.send("Please specify a user")

def setup(bot): # this will add this file to the cogs 
  bot.add_cog(mod(bot))