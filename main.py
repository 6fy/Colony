from discord.ext import commands
import discord

with open('assets/configuration/' + 'config.0', 'r') as f:
  lines = f.readlines()
  token = lines[0]
  prefix = lines[1]

client = commands.Bot(command_prefix=prefix)

@client.event
async def on_ready():
  print(f"{client.user} has launched!")
  
cogs = {
  'cogs.duits',
  'cogs.mod',
  'cogs.eco',
}

if __name__ == "__main__":
  for cog in cogs:
    client.load_extension(cog)
    print(f"{cog} has been loaded")

client.run(token, bot=True)