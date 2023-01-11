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
