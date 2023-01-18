# bot.py
import os
import discord
from discord.ext import commands

import sys
print("sys.path:\n" + "\n".join(sys.path))

import random
from APICall import getRhymeWords 

######### DO NOT CHANGE #########
import os.path
with open(os.path.dirname(__file__) + "/../TOKEN.txt","r") as f:
    TOKEN = f.readline().rstrip()
with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
    BRANCH = f.readline().rstrip()
#################################
    
client = commands.Bot(intents=discord.Intents.all(),command_prefix="!")


############# GIT ###############
import subprocess
@client.command()
async def git(ctx, *args):
    if len(args) == 0:
        embedVar = discord.Embed(title="Git", description="Possible commands", color=0xff0000)
        embedVar.add_field(name="!git status", value="Current branch the bot is in", inline=False)
        embedVar.add_field(name="!git checkout [branch]", value="Checkout a different branch. RELOAD ON EXECUTION", inline=False)
        await ctx.send(embed=embedVar)  
    elif args[0] == "status":
        message = f"Currently on branch '{BRANCH}'"
        with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
            newbranch = f.readline().rstrip()
        if newbranch != BRANCH:
            message += f"\nAfter reboot on branch '{newbranch}'"
        await ctx.send(message)
        
    elif args[0] == "checkout":
        with open(os.path.dirname(__file__) + "/../branch.txt","w") as f:
            f.write(args[1])
        await ctx.send(f"After reboot, starting up on branch '{args[1]}'")
#################################

####### DEPENDENCIES ############
@client.command()
async def pip(ctx, *args):
    if len(args) == 0:
        embedVar = discord.Embed(title="Pip", description="Possible commands", color=0x0000ff)
        embedVar.add_field(name="!pip install", value="Installs a package", inline=False)
        embedVar.add_field(name="!pip uninstall", value="Uninstalls a package", inline=False)
        await ctx.send(embed=embedVar)
    elif args[0] == "install":
        output = subprocess.check_output(f"sudo pip install {args[1]}", shell=True)
        await ctx.send(output.decode("utf-8") ) 
    elif args[0] == "uninstall":
        output = subprocess.check_output(f"sudo pip uninstall {args[1]}", shell=True)
        await ctx.send(output.decode("utf-8") ) 
#################################

@client.command()
async def reload(ctx, *args):
    await ctx.channel.send("Rebooting...")
    await client.change_presence(activity=discord.Game(name="Rebooting..."))
    os.system("sudo reboot")

@client.command()
async def rhyme(ctx, *args):
    
    ## HELP
    if len(args) == 0:
        embedVar = discord.Embed(title="Rhyme bot", description="Possible commands", color=0x00ff00)
        embedVar.add_field(name="!rhyme [phrase]", value="Receive a random rhyme word", inline=False)
        embedVar.add_field(name="!rhyme [phrase] -all", value="Receive all rhyme words", inline=False)
        embedVar.add_field(name="!rhyme [phrase] -best [x=1]", value="Receive the best x rhyme words. By default: 1", inline=False)
        embedVar.add_field(name="!rhyme [phrase] -worst [x=1]", value="Receive the worst x rhyme words. By default: 1", inline=False)
        await ctx.send(embed=embedVar)  
    
    else:
        rhymeWords = getRhymeWords([x for x in args if x[0] != "-"][-1])
    
        # No rhyme words found:
        if len(rhymeWords) == 0:
            await ctx.channel.send(f"No words found that rhyme with '{args[0]}'")

        elif "-all" in args:
            await ctx.channel.send(', '.join(rhymeWords))

        elif "-best" in args:
            if len(args) > 2:
                await ctx.channel.send(', '.join(rhymeWords[:int(args[-1])]))
            else:
                await ctx.channel.send(rhymeWords[0])
        elif "-worst" in args:
            if len(args) > 2:
                await ctx.channel.send(', '.join(rhymeWords[-int(args[-1]):]))
            else:
                await ctx.channel.send(rhymeWords[-1])
        else:
            await ctx.channel.send(random.choice(rhymeWords))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=f"Active>{BRANCH}"))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    

    await client.process_commands(message)
                
            
client.run(TOKEN)
