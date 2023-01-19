import interactions
import os
import sys
import discord
print("sys.path:\n" + "\n".join(sys.path))

import random
from APICall import getRhymeWords 

######### DO NOT CHANGE #########
import os.path
with open(os.path.dirname(__file__) + "/../TOKEN.txt","r") as f:
    TOKEN = f.readline().rstrip()
with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
    BRANCH = f.readline().rstrip()
_ready = False
#################################

GUILD = 1038035076509880342

bot = interactions.Client(token=TOKEN)

@bot.command(
    name="base_command",
    description="This description isn't seen in UI (yet?)",
    scope=GUILD,
    options=[
        interactions.Option(
            name="command_name",
            description="A descriptive description",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="option",
                    description="A descriptive description",
                    type=interactions.OptionType.INTEGER,
                    required=False,
                ),
            ],
        ),
        interactions.Option(
            name="second_command",
            description="A descriptive description",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="second_option",
                    description="A descriptive description",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ],
        ),
    ],
)
async def cmd(ctx: interactions.CommandContext, sub_command: str, second_option: str = "", option: int = None):
    if sub_command == "command_name":
        await ctx.send(f"You selected the command_name sub command and put in {option}")
    elif sub_command == "second_command":
        await ctx.send(f"You selected the second_command sub command and put in {second_option}")
        

############# GIT ###############
import subprocess
@bot.command(
    name="git",
    description="Use git commands to switch branches and check current branch",
    scope=GUILD,
    options=[
        interactions.Option(
            name="help",
            description="Overview of all commands",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="status",
            description="Check current branch of the bot",
            type=interactions.OptionType.SUB_COMMAND,
        ),
        interactions.Option(
            name="checkout",
            description="Switch to another branch",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="branch",
                    description="New branch",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ],
        ),
    ],
)
async def git(ctx: interactions.CommandContext, sub_command: str, branch: str = ""):
    if sub_command == "help":
        embedVar = discord.Embed(title="Git", description="Possible commands", color=0xff0000)
        embedVar.add_field(name="!git status", value="Current branch the bot is in", inline=False)
        embedVar.add_field(name="!git checkout [branch]", value="Checkout a different branch. RELOAD ON EXECUTION", inline=False)
        await ctx.send(embed=embedVar)  
    
    elif sub_command == "status":
        message = f"Currently on branch '{BRANCH}'"
        with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
            newbranch = f.readline().rstrip()
        if newbranch != BRANCH:
            message += f"\nAfter reboot on branch '{newbranch}'"
        await ctx.send(message)
        
    elif sub_command == "checkout":
        with open(os.path.dirname(__file__) + "/../branch.txt","w") as f:
            f.write(branch)
        await ctx.send(f"After reboot, starting up on branch '{branch}'")
#################################

      
      
@bot.command(
    name="reboot",
    description="Reboots the server to add recent changes",
    scope=GUILD,
)
async def reload(ctx):
    await ctx.send("Rebooting...")
    #await bot.change_presence(presence=interactions.ClientPresence("Rebooting..."))
    os.system("sudo reboot")        


@bot.event
async def on_ready():
    global _ready
    if not _ready:
        #await bot.change_presence(presence=interactions.ClientPresence(f"Active on '{BRANCH}'"))
        print(f'{bot.user} has connected to Discord!')  
        _ready = True
          
bot.start()