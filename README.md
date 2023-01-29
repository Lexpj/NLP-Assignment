# Discord Rhymebot

This is a GitHub repo containing the code for a discord bot that can produce rhyme sentences based on a given prompt. It uses an [API](https://www.datamuse.com/api/) to fetch possible rhyme words and can, via model of selection (BART/T5), produce a rhyme sentence that it will send back. After that, there is the possibility to score the sentence using BLEU.

## Set up
There are several things to do before you can make use of this code. First of all, this code was originally produced on Linux. In order to make use of the GitHub, Pip and reboot commands, you need to setup a service:

In your `/etc/system/systemd` folder, place the provided `DiscordBot.service` script. Be sure to change the `ExecStart` path to the path where your shell script is.

The shell script provided clones the repository branch the bot is currently on. It then starts `bot.py` that is in that folder. Also here, make sure to change the paths in `startbot` to wherever this repo is placed.

Furthermore, the folder at the root of NLP-Assignment, must contain 2 additional text files as well as any dataset. 
- `branch.txt` must be placed outside of the project, since this file is changed when calling `/git status` in the discord bot. This file contains the branch that is cloned when starting the bot.
- `TOKEN.txt` must be placed outside of the project, since this contains the token for the discord bot to connect to discord services. Exposing this token exposes the account the bot is connected to, and anyone may then make use of your bot and/or account. BE CAREFUL NOT TO EXPOSE THIS.
- Any dataset must be placed outside of the project, since these are often too large for GitHub to handle and or unnecessary to push to GitHub in the first place. In this case, for calculating the BLEU score, `bbc.lines` is placed outside the GitHub project.

Lastly, as briefly mentioned, a discord bot has to be made at [the developer website](https://discord.com/developers/applications) of Discord. Here, you create an application and use the token of that application in this bot. You can then also create an invite link for your bot to your preferred server. Make sure it has at least `default intents`. Check a tutorial when you are stuck.

Install the required packages by:
```
pip install -r requirements.txt
```

When the setup is complete, you can start your bot with 
```
sudo systemctl start DiscordBot
```
or simply reboot your device. This script starts whenever the device has made a connection to internet once rebooted.

## Usage
This bot makes use of the new SlashCommands discord has provided, and uses the package `interactions.py` to make this possible. Typing / in your server will show the commands the bot can do. These are the following:

These are production commands:
- /git status: Sends back on which branch the bot currently operates.
- /git checkout [branch]: Changes the bot to a different branch. After this, a reboot is needed to start it up on that branch
- /pip install [package]: Installs a package to the bot using Pip
- /pip uninstall [package]: Uninstalls a package using Pip
- /reboot: Reboots the DiscordBot.service program

These are user commands:
- /rhyme [prompt]: The user gives a prompt, like a sentence or a phrase, to receive a number of rhyming sentences back. Punctuation matters: ending in a comma, dot, question mark, exclamation mark or no punctuation can change the results! After this, you can press `Continue rhyming` to get the next possible rhyme words.
- /rhymewords [word]: Returns a random rhyme word. You also get the button options to get the best, worst or all rhyme words for the given word. 

In `bot.py`, change the model to your own version of a model to test it out. Have fun!

## Questions
For questions or issues, open an issue.