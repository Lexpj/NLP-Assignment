# bot.py
import os
import discord
from discord.ext import commands

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
    ctx.channel.send("Rebooting...")
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
    
    elif "-all" in args[1:]:
        await ctx.channel.send(', '.join(getRhymeWords(args[0])))
    elif "-best" in args[1:]:
        if len(args) > 2:
            await ctx.channel.send(', '.join(getRhymeWords(args[0])[:int(args[2])]))
        else:
            await ctx.channel.send(getRhymeWords(args[0])[0])
    elif "-worst" in args[1:]:
        if len(args) > 2:
            await ctx.channel.send(', '.join(getRhymeWords(args[0])[-int(args[2]):]))
        else:
            await ctx.channel.send(getRhymeWords(args[0])[-1])
    else:
        await ctx.channel.send(random.choice(getRhymeWords(args[0])))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    
    if message.author == client.user:
        return
    

    await client.process_commands(message)
                
            
client.run(TOKEN)
