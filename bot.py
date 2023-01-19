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
#################################

GUILD = 1038035076509880342

bot = interactions.Client(token=TOKEN)
bot.change_presence()

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
        
      
      
@bot.command(
    name="reboot",
    description="Reboots the server to add recent changes",
    scope=GUILD,
)
async def reload(ctx, *args):
    await ctx.channel.send("Rebooting...")
    await bot.change_presence(presence=interactions.ClientPresence("Rebooting..."))
    os.system("sudo reboot")        


@bot.event
async def on_ready():
    await bot.change_presence(presence=interactions.ClientPresence(f"Active on '{BRANCH}'"))
    print(f'{bot.user} has connected to Discord!')        
        
bot.start()