import interactions
import os
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
_ready = False
#################################

GUILD = 1038035076509880342
rhymeWords = []

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
@bot.command(
    name="git",
    description="Use git commands to switch branches and check current branch",
    scope=GUILD,
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
    scope=GUILD,
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

@bot.command(
    name="rhyme",
    description="Use rhyme commands",
    scope=GUILD,
    options=[
        interactions.Option(
            name="prompt",
            description="Sentence/phrase/word to rhyme",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)

async def rhyme(ctx: interactions.CommandContext, sub_command: str = None, prompt: str = "", items: int = 1):
    global rhymeWords
    rhymeWords = getRhymeWords(prompt.split()[-1])
    
    if len(rhymeWords) == 0:
        await ctx.send(f"No words found that rhyme with '{prompt.split()[-1]}'")
    await ctx.send(random.choice(rhymeWords),components=row)
   
@bot.component("all")
async def button_reponse_all(ctx):
    await ctx.send(', '.join(rhymeWords))

@bot.component("worst")
async def button_reponse_worst(ctx):
    await ctx.send(rhymeWords[-1])
    
@bot.component("best")
async def button_reponse_best(ctx):
    await ctx.send(rhymeWords[0])

#####################################
   
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
        print(f'Bot has connected to Discord!')  
        _ready = True
          
bot.start()