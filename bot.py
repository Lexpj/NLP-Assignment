import interactions
import os
import random
from APICall import getRhymeWords, checkName, checkWord
from BART import BART
from BLEU import BLEU
from TFIVE import Tfive
from threading import *

BARTJUH = Tfive()
#BLEUTJUH = BLEU()

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
buttonReRhyme = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Continue rhyming",
    custom_id="rerhyme"
)


row = interactions.ActionRow(components=[buttonAll,buttonWorst,buttonBest])
rhymeon = interactions.ActionRow(components=[buttonReRhyme])


def __jobBart(ctx,prompt,rhymeword):
    global q
    gen = BARTJUH.gen(prompt,rhymeword)[0]
    try:
        q[prompt].append((gen,ctx,rhymeword,0))#BLEUTJUH.score(gen)))
    except:
        q[prompt] = [(gen,ctx,rhymeword,0)]#BLEUTJUH.score(gen))]
    


# Checks whether the sentence is correct.
def CheckSentence(prompt: str):
    fullStopCount = 0
    words = prompt.split()
    # Count how many full stops or other stops there are in the given prompt
    for word in words:
        word = word.replace(".","").replace(",","").replace("?","").replace("!","")
        # Check if word is in English dictionary or name dictionary
        if checkWord(word) == 0:
            if checkName(word) == 0:
                # Check if user wants to continue, gives the option yes to continue or no to restart
                return f"'{word}' can not be found in the dictionary database, are you sure this is correct?"
        # Checking every character in a word
        for char in word:
            if char in (".", "?", "!"):
                fullStopCount += 1
        # If there are multiple full or other stops detected (more than 1)
        if fullStopCount >= 2:
            return f"Multiple full stops are detected, is this a single sentence? Try to send a single sentence."
    return ""



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
    blacklist = []
    
    # Check input
    res = ""#CheckSentence(prompt) 
    if res != "":
        await ctx.send(res)
        return

    # Remove punctuation at last word
    if prompt[-1] in ".,?!":
        newprompt = prompt[:-1]
    else:
        newprompt = prompt
    blacklist.append(newprompt.split()[-1])
    rhymeWords = getRhymeWords(newprompt.split()[-1], blacklist)
    
    if len(rhymeWords) == 0:
        await ctx.send(f"No words found that rhyme with '{prompt.split()[-1]}'")
    else:
        await ctx.defer()
        
        threads = [Thread(target=__jobBart,args=(ctx,prompt,rhymeWords[i])) for i in range(min(5,len(rhymeWords)))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        k = list(q.keys()).copy()
        for item in k:
            res = q.get(item,None)
            s = f"{item} \n"
            if res != None:
                for i in q[item]:
                    try:
                        #s += '({0:.2f}'.format(i[3]) + f",{i[2]})" + f": {i[0]}\n"
                        s += f"({i[2]})" + f": {i[0]}\n"
                    except Exception as e:
                        print(e)
                await q[item][0][1].send(s,components=rhymeon)
            try:
                del q[item]
            except:pass
                                    
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
    phrase = extractPhrase(str(ctx.message.content))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"All rhymes of '{word}' are: {', '.join(rhymes)}",components=row)

@bot.component("worst")
async def button_reponse_worst(ctx):
    phrase = extractPhrase(str(ctx.message.content))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"The worst rhyme of '{word}' is {rhymes[-1]}",components=row)
    
@bot.component("best")
async def button_reponse_best(ctx):
    phrase = extractPhrase(str(ctx.message.content))
    word = phrase.split()[-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"The best rhyme of '{word}' is {rhymes[0]}",components=row)

@bot.component("rerhyme")
async def button_response_rerhyme(ctx):
    phrase = str(ctx.message.content)
    print(phrase)
    phrase = phrase.split('\n')[0]
    word = phrase.split()[-1]
    if word[-1] in ".,?!":
        word = word[:-1]
    rhymes = getRhymeWords(word)
    await ctx.send(f"To continue, '{word}' rhymes with: {', '.join(rhymes)}",components=rhymeon)

#####################################
   
# @bot.command(
#     name="reboot",
#     description="Reboots the server to add recent changes",
# )
# async def reload(ctx):
#     await ctx.send("Rebooting...")
#     with open(os.path.dirname(__file__) + "/../branch.txt","r") as f:
#         branch = f.readline().rstrip()
#     await bot.change_presence(presence=interactions.api.models.presence.ClientPresence(activities=[
#         interactions.api.models.presence.PresenceActivity(name=f"Rebooting to '{branch}'...",type=0)
#     ]))
#     os.system("sudo systemctl restart DiscordBot")        
        
@bot.event
async def on_ready():
    global _ready
    if not _ready:
        #await bot.change_presence(presence=interactions.api.models.presence.ClientPresence(activities=[
        #    interactions.api.models.presence.PresenceActivity(name=f"Active on '{BRANCH}'",type=0)
        #]))
        print(f'Bot has connected to Discord!')  
        _ready = True
            
bot.start()
