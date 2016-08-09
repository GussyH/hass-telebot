# hass-telebot
Bot for the Telegram messaging platform providing an interface to the Home Assistant automation system

## Instructions

Download hass-telebot.py and install in a python virtualenv

You may need to 'pip3 install' a few things (like homeassistant, telepot, argparse, configobj)

Create hass-telebot.cfg with entries as follows:

```
ha_url = "<hass host - no http/htts>"
ha_key = "<you api password if any>"
ha_port = "<hass port>"
ha_ssl = "<true or false, depending on whether you are running ssl or not>"
ha_alarm_code = "<the alarm code you use for the alarm_control_panel component>"
bot_token = "<the token for your Telegram bot>"
allowed_chat_id = "<chat id from the Telegram chat in which you are talking to your bot>"
```

Then you can run the bot with

```
./hass-telebot.py hass-telebot.cfg
```

## Usage

The bot will only respond to you if you are talking to it in the specified chat denoted in the config file.

Currrent commands are
```
/roll
/states
/menu (brings up a custom keyboard of the other commands)
/alarm (brings up a custom keyboard of alarm controls)
/alarmhome
/alarmaway
/disarm
```
For now you need to edit the code to put the entitities you want to see in /states
```
devices = ['alarm_control_panel.ha_alarm']
```

## Service/Daemon Mode
Erm right now I've not done anything for this. I just been running it the background with nohup :)
