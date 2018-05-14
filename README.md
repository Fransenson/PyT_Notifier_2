# PyT_Notifier_2
Open Source lightweight Telegram notifications for Profittrailer 2



## Features
* Telegram push notifications with detailed information on buys(normal and DCA) and sales
* NO EXCHANGE API REQUIRED - all information is being read from the PT database
* Support for multiple PT Instances


Future:
* Custom designed messages..by you via the settings!
* additional information via notifications outside of actual transaction
* ask the bot to give you statistics about your current holdings

## Installation

**If you've installed Python(3.X) already, you can probably skip to step 2**

### Step 1 - Install Python
Install Python 3: Follow the instructions on [the Python download page](https://www.python.org/downloads/)

____


### Step 2 - Download PyT_Notifier
Download the current version of PyT_Notifier from the [release page here on GitHub](https://github.com/Fransenson/PyT_Notifier_2/releases)

____
### Step 3 - Change settings as needed
Open `settings.py` with a text editor of your choice and fill in your relevant data. 

If you don't have a Telegram Bot API key already, go ask @BotFather on Telegram about it.

To get your chat id, open a chat with your bot, visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates` in a browser, send the bot a message and refresh the page.

Please provide absolute paths to the needed JSON-Files. 

Format for 1 bot instance: 
```
{0: {"name": "NameOfInstance", "path": "/path/to/ProfitTrailerData.json"}}
```
Format for multiple bot instances: 
```
{0: {"name": "NameOfInstance", "path": "/path/to/ProfitTrailerData.json"}, 1: {"name": "NameOfInstance2", "path": "/path/to/second/ProfitTrailerData.json"}}
```

____
### Step 4 - Run!
Run the script via `python3 PyT_Notifier_2.py` in your terminal.

If you are using pm2 just go with `pm2 start PyT_Notifier_2.py --interpreter python3`

____
## Feedback
Please report any issues here on GitHub. 

If you want to buy me a coffee (or a sports car):

BTC: 15Xh2nAhXqSkTMczRt6g8HFGtuzE7Keab7

ETH: 0x1a635457f7773fcb2c0e9001669eb540672a240f

Those would be tips/donations only. The software is distributed free of charge and I don't offer paid support. I will try to help where I can though!

Thanks!
