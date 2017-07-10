# hass-telebot
Bot for the Telegram messaging platform providing an interface to the Home Assistant automation system
Built using Telepot (http://telepot.readthedocs.io/en/latest/). That doc has instuctions for creating your bot and talking to it for the first time to get chat ids.

## Instructions

Download hass-telebot.py and install in a python virtualenv

Install requirements:
```
pip3.5 install -r requirements.txt
```

Create hass-telebot.cfg with entries as follows:

```
ha_url = "<hass host/ip - no http/https>"
ha_key = "<you api password if any>"
ha_port = "<hass port>"
ha_ssl = "<true or '', depending on whether you are running ssl or not>"
ha_alarm_entity = "<e.g. alarm_control_panel.ha_alarm>"
ha_alarm_code = "<the alarm code you use for the alarm_control_panel component>"
bot_token = "<the token for your Telegram bot>"
allowed_chat_ids = "<list of Telegram chat ids in which you are talking to your bot>"
fav_entities = "<space separated list of favourite entities (used by /favstates)>"
show_maps = "<true or false whether you want maps to show for device locations>"
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
/favstates (tells you the state of your favourite entities)
/menu (brings up a custom keyboard of the other commands)
/refreshservices (refreshes the list of domains/services from HASS)
/domains (lists the current HASS domains)
/browsedomains (presents the domains as a custom keyboard - start of dynamic browsing)
/alarm (brings up a custom keyboard of alarm controls, based on alarm state)
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
