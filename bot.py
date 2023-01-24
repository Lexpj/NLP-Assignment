import interactions
import os
import sys
print("sys.path:\n" + "\n".join(sys.path))
import subprocess
import random
from APICall import getRhymeWords 
from BART import BART
from threading import *

BARTJUH = BART()

######### DO NOT CHANGE #########
import os.path
with open(os.path.dirname(__file__) + "/../TOKEN.txt","r") as f:
    TOKEN = f.readline().rstrip()
with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
    BRANCH = f.readline().rstrip()
_ready = False
q = {}

#################################

bot = interactions.Client(token=TOKEN)

############# GIT ###############

@bot.command(
    name="git",
    description="Use git commands to switch branches and check current branch",
    options=[
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
    if sub_command == "status":
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

############# PIP ###############
@bot.command(
    name="pip",
    description="Use pip commands to install or uninstall packages",
    options=[
        interactions.Option(
            name="install",
            description="Install a package",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="package",
                    description="Package to be installed",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ],
        ),
        interactions.Option(
            name="uninstall",
            description="Uninstall a package",
            type=interactions.OptionType.SUB_COMMAND,
            options=[
                interactions.Option(
                    name="package",
                    description="Package to be uninstalled",
                    type=interactions.OptionType.STRING,
                    required=True,
                ),
            ],
        ),
    ],
)
async def pip(ctx: interactions.CommandContext, sub_command: str, package: str = ""):
    if sub_command == "install":
        os.system(f"sudo pip install {package}")
        await ctx.send(f"{package} installed!") 
    elif sub_command == "uninstall":
        os.system(f"sudo pip uninstall {package}")
        await ctx.send(f"{package} installed!")  
#################################  


############ RHYME ##############

buttonAll = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="All",
    custom_id="all"
)
buttonBest = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Best",
    custom_id="best"
)
buttonWorst = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Worst",
    custom_id="worst"
)
row = interactions.ActionRow(components=[buttonAll,buttonWorst,buttonBest])


def __jobBart(ctx,prompt,rhymeWords):
    global q
    gen = BARTJUH.gen(prompt,rhymeWords[0])
    q[prompt] = (gen,ctx)
    
    
@bot.command(
    name="rhyme",
    description="Use rhyme commands",
    options=[
        interactions.Option(
            name="prompt",
            description="Sentence/phrase/word to rhyme",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)    

async def rhyme(ctx: interactions.CommandContext, prompt: str = ""):
    global q
    if prompt[-1] in ".,?!":
        newprompt = prompt[:-1]
    else:
        newprompt = prompt
    rhymeWords = getRhymeWords(newprompt.split()[-1])
    
    if len(rhymeWords) == 0:
        await ctx.send(f"No words found that rhyme with '{prompt.split()[-1]}'")
    else:
        await ctx.defer()
        
        thread = Thread(target=__jobBart,args=(ctx,prompt,rhymeWords))
        
        thread.start()
        thread.join()
        
        k = list(q.keys()).copy()
        for item in k:
            res = q.get(item,None)
            if res != None:
                try:
                    await q[item][1].send(f"{item} \n-> {q[item][0]}")
                    del q[item]
                except Exception as e:
                    print(e)
                    
@bot.command(
    name="rhymewords",
    description="Get single rhyme word",
    options=[
        interactions.Option(
            name="prompt",
            description="Sentence/phrase/word to rhyme",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)    
async def rhymewords(ctx: interactions.CommandContext, prompt: str = ""):

    if prompt[-1] in ".,":
        newprompt = prompt[:-1]
    else:
        newprompt = prompt
    rhymeWords = getRhymeWords(newprompt.split()[-1])
    
    if len(rhymeWords) == 0:
        await ctx.send(f"No words found that rhyme with '{prompt.split()[-1]}'")
    else:
        await ctx.send(f"'{prompt}' rhymes with {random.choice(rhymeWords)}",components=row)
        
        

def extractPhrase(s,word=False):
    phrase = ""
    quotes = 0
    for chr in s:
        if chr == "'":
            quotes += 1
        elif quotes == 1:
            phrase += chr
    return phrase


@bot.component("all")
async def button_reponse_all(ctx):
    phrase = extractPhrase(str(ctx.message))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"All rhymes of '{word}' are: {', '.join(rhymes)}",components=row)

@bot.component("worst")
async def button_reponse_worst(ctx):
    phrase = extractPhrase(str(ctx.message))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"The worst rhyme of '{word}' is {rhymes[-1]}",components=row)
    
@bot.component("best")
async def button_reponse_best(ctx):
    phrase = extractPhrase(str(ctx.message))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"The best rhyme of '{word}' is {rhymes[0]}",components=row)

#####################################
   
@bot.command(
    name="reboot",
    description="Reboots the server to add recent changes",
)
async def reload(ctx):
    await ctx.send("Rebooting...")
    with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
        branch = f.readline().rstrip()
    await bot.change_presence(presence=interactions.api.models.presence.ClientPresence(activities=[
        interactions.api.models.presence.PresenceActivity(name=f"Rebooting to '{branch}'...",type=0)
    ]))
    os.system("sudo systemctl restart DiscordBot")        
        
@bot.event
async def on_ready():
    global _ready
    if not _ready:
        await bot.change_presence(presence=interactions.api.models.presence.ClientPresence(activities=[
            interactions.api.models.presence.PresenceActivity(name=f"Active on '{BRANCH}'",type=0)
        ]))
        print(f'Bot has connected to Discord!')  
        _ready = True
            
bot.start()
