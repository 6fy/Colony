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
  # message = 'Dit is geen carlos dit is een duits botje!'
  # for guild in client.guilds:
  #   for channel in guild.channels:
  #     if channel.type == discord.ChannelType.text:
  #       if "general" in channel.name:
  #         await channel.send(message)
  #         print(f'Sent "{message}" to {channel.name} in {guild.name}')

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