# bot.py
import os
import sys
print("sys.path:\n" + "\n".join(sys.path))

import random
from APICall import getRhymeWords 

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

@tree.command(guild = GUILD, name = 'test', description='options')
@app_commands.describe(option="This is a description of what the option means")
@app_commands.choices(option=[
        app_commands.Choice(name="Option 1", value="1"),
        app_commands.Choice(name="Option 2", value="2")
    ])
async def test(ctx, option, *args):
    await ctx.response.send_message(f"Options {option}, args {args}", ephemeral = True) 


@tree.command(guild = GUILD, name = 'git', description='Git commands for the branch the bot works on')
@app_commands.describe(option="Git argument")
@app_commands.choices(option=[
        app_commands.Choice(name="help", value="help"),
        app_commands.Choice(name="checkout", value="checkout"),
        app_commands.Choice(name="status", value="status")
    ])
async def git(ctx, option, *args):
    if option == "help":
        embedVar = discord.Embed(title="Git", description="Possible commands", color=0xff0000)
        embedVar.add_field(name="/git status", value="Current branch the bot is in", inline=False)
        embedVar.add_field(name="/git checkout [branch]", value="Checkout a different branch. RELOAD ON EXECUTION", inline=False)
        await ctx.send(embed=embedVar)  
    elif option == "status":
        message = f"Currently on branch '{BRANCH}'"
        with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
            newbranch = f.readline().rstrip()
        if newbranch != BRANCH:
            message += f"\nAfter reboot on branch '{newbranch}'"
        await ctx.send(message)
        
    elif option == "checkout":
        with open(os.path.dirname(__file__) + "/../branch.txt","w") as f:
            f.write(option)
        await ctx.send(f"After reboot, starting up on branch '{option}'")




aclient.run(TOKEN)
