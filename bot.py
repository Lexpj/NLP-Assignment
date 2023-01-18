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
#################################
    
client = commands.Bot(intents=discord.Intents.all(),command_prefix="!")


############# GIT ###############
import subprocess
@client.command()
async def git(ctx, *args):
    if len(args) == 0:
        embedVar = discord.Embed(title="Git", description="Possible commands", color=0xff0000)
        embedVar.add_field(name="!git status", value="Current branch the bot is in", inline=False)
        embedVar.add_field(name="!git checkout [branch]", value="Checkout a different branch", inline=False)
        embedVar.add_field(name="!git pull", value="Pulls current branch", inline=False)
        await ctx.send(embed=embedVar)  
    elif args[0] == "status":
        output = subprocess.check_output("cd /home/pi/Desktop/nlp/NLP-Assignment; git status", shell=True)
        await ctx.send(output) 
    elif args[0] == "checkout":
        output = subprocess.check_output(f"cd /home/pi/Desktop/nlp/NLP-Assignment; git checkout {args[1]}", shell=True)
        await ctx.send(output) 
    elif args[0] == "pull":
        output = subprocess.check_output("cd /home/pi/Desktop/nlp/NLP-Assignment; git pull", shell=True)
        await ctx.send(output) 
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
        await ctx.send(output) 
    elif args[0] == "uninstall":
        output = subprocess.check_output(f"sudo pip uninstall {args[1]}", shell=True)
        await ctx.send(output) 
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
        embedVar.add_field(name="!rhyme [word]", value="Receive a random rhyme word", inline=False)
        embedVar.add_field(name="!rhyme [word] -all", value="Receive all rhyme words", inline=False)
        embedVar.add_field(name="!rhyme [word] -best [x=1]", value="Receive the best x rhyme words. By default: 1", inline=False)
        embedVar.add_field(name="!rhyme [word] -worst [x=1]", value="Receive the worst x rhyme words. By default: 1", inline=False)
        await ctx.send(embed=embedVar)  
    
    else:
        rhymeWords = getRhymeWords(args[0])
    
        # No rhyme words found:
        if len(rhymeWords) == 0:
            await ctx.channel.send(f"No words found that rhyme with '{args[0]}'")

        elif "-all" in args[1:]:
            await ctx.channel.send(', '.join(rhymeWords))

        elif "-best" in args[1:]:
            if len(args) > 2:
                await ctx.channel.send(', '.join(rhymeWords[:int(args[2])]))
            else:
                await ctx.channel.send(rhymeWords[0])
        elif "-worst" in args[1:]:
            if len(args) > 2:
                await ctx.channel.send(', '.join(rhymeWords[-int(args[2]):]))
            else:
                await ctx.channel.send(rhymeWords[-1])
        else:
            await ctx.channel.send(random.choice(rhymeWords))

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Active"))
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    

    await client.process_commands(message)
                
            
client.run(TOKEN)
