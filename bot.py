




import discord
from discord import app_commands 

######### DO NOT CHANGE #########
import os.path
with open(os.path.dirname(__file__) + "/../TOKEN.txt","r") as f:
    TOKEN = f.readline().rstrip()
with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
    BRANCH = f.readline().rstrip()
GUILD = discord.Object(id=1038035076509880342)
#################################

class client(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False #we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced: #check if slash commands have been synced 
            await tree.sync(guild=GUILD) #guild specific: leave blank if global (global registration can take 1-24 hours)
            self.synced = True
        print(f"We have logged in as {self.user}.")
        await self.change_presence(activity=discord.Game(name=f"Active on '{BRANCH}'"))

aclient = client()
tree = app_commands.CommandTree(aclient)

@tree.command(guild = GUILD, name = 'tester', description='testing') #guild specific slash command
async def slash2(interaction: discord.Interaction):
    await interaction.response.send_message(f"I am working! I was made with Discord.py!", ephemeral = True) 

aclient.run(TOKEN)
