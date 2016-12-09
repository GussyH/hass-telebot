#!/srv/telebot/bin/python3.5
import time
import random
import datetime
import telepot
import argparse
from configobj import ConfigObj
import homeassistant.remote as remote

# Get command line args
parser = argparse.ArgumentParser()

parser.add_argument("config", help="full path to config file", type=str)
args = parser.parse_args()
config_file = args.config

# Read Config File
config = ConfigObj(config_file, file_error=True)

ha_url = config['ha_url']
ha_key = config['ha_key']
ha_port = config['ha_port']
ha_ssl = config['ha_ssl']
ha_alarm_entity = config['ha_alarm_entity']
ha_alarm_code = config['ha_alarm_code']
bot_token = config['bot_token']
allowed_chat_ids = config['allowed_chat_ids']
fav_entities = config['fav_entities']
fav_entities = fav_entities.split()
show_maps = config['show_maps']

# instance the API connection to HASS
api = remote.API(ha_url, ha_key, ha_port, ha_ssl)
print(remote.validate_api(api))

# this prints out all the HASS services - mostly here for testing atm
print('-- Available Domains/Services:')
services = remote.get_services(api)
for service in services:
    print(service['domain'])
    print(service['services'])

# instance the Telegram bot
bot = telepot.Bot(bot_token)

# calls the HASS API to get the state of an entity
# need to change this so you can pass in entity type so we can get the right attributes for display
def get_state (entity_id, readable):
  print(entity_id)
  entity = remote.get_state(api, entity_id)
  if (readable == 'true'):
    state = format('{} is {}.'.format(entity.attributes['friendly_name'], entity.state))
  else:
    state = entity.state
  print(state)
  return state
  
# sends the location from any entity
def send_location(chat_id, entity_id):
  entity = remote.get_state(api, entity_id)
  if (show_maps == 'true' and entity.state != 'home' and
      'latitude' in entity.attributes and
      'longitude' in entity.attributes):  
    latitude = float(entity.attributes['latitude'])
    longitude = float(entity.attributes['longitude'])

    bot.sendLocation(chat_id=chat_id,
                     latitude=latitude, longitude=longitude)

# calls a HASS service
def service_call (domain, service, payload):
  remote.call_service(api, domain, service, payload)

def refresh_services ():
  services = remote.get_services(api)
  for service in services:
    print(service['domain'])
    #print(service['services'])

# handle the incoming Telegram message
def handle(msg):

    # glance to get some meta on the message
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    # we only want to process text messages from our specified chat
    if (content_type == 'text') and (str(chat_id) in allowed_chat_ids):
      command = msg['text']

      print(command)

      if command == '/roll':
          bot.sendMessage(chat_id, random.randint(1,6))
      elif command == '/time':
          bot.sendMessage(chat_id, str(datetime.datetime.now()))
      elif command == '/start':
          bot.sendMessage(chat_id, 'hola!')
      elif command == '/refreshservices':
          # refreshes the list of available domains/services from the server
          refresh_services()
          bot.sendMessage(chat_id, "Service list refreshed")
      elif command == '/domains':
          # lists avaiable domains
          domain_str = ""
          for service in services:
            domain_str = domain_str + service['domain'] + '\n'
          bot.sendMessage(chat_id,domain_str)
      elif command == '/browsedomains':
          # lists avaiable domains on custom keyboard
          keyboard = []
          for service in services:
            key_item = [{"text":service['domain']}]
            keyboard.append(key_item)

          replymarkup = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": True
          }
          bot.sendMessage(chat_id,"Pick a domain....",reply_markup=replymarkup)
      elif command == '/favstates':
          for s in fav_entities:
            state = get_state(s,'true')
            bot.sendMessage(chat_id, state)
            send_location(chat_id, s)
      elif command == '/armhome':
          payload = {'code': ha_alarm_code}
          service_call('alarm_control_panel','alarm_arm_home',payload)
          bot.sendMessage(chat_id, 'Home alarm mode should be pending')
      elif command == '/armaway':
          payload = {'code': ha_alarm_code}
          service_call('alarm_control_panel','alarm_arm_away',payload)
          bot.sendMessage(chat_id, 'Away alarm mode should be pending')
      elif command == '/disarm':
          payload = {'code': ha_alarm_code}
          service_call('alarm_control_panel','alarm_disarm',payload)
          bot.sendMessage(chat_id, 'You are welcome!')
      elif command == '/alarm':
          # check the current state of the alarm so we can decide what options to show
          alarm_state = get_state(ha_alarm_entity,'false')
          if (alarm_state == 'disarmed'):
            keyboard = [[{"text":"/armhome"}], [{"text":"/armaway"}]]
          else:
            keyboard = [[{"text":"/disarm"}]]

          replymarkup = {
            "keyboard": keyboard,
            "resize_keyboard": True,
            "one_time_keyboard": True
          }
          bot.sendMessage(chat_id, 'Alarm currently ' + alarm_state + '.\nPlease choose an option:',reply_markup=replymarkup)
      elif command == '/menu':
          replymarkup = {
            "keyboard": [[{"text":"/alarm"}], [{"text":"/favstates"}], [{"text":"/roll"}]],
            "resize_keyboard": True,
            "one_time_keyboard": True
          }
          bot.sendMessage(chat_id, 'Please choose an option...',reply_markup=replymarkup)
    elif (content_type == 'text') and (str(chat_id) not in allowed_chat_ids):
        bot.sendMessage(chat_id, 'You are not authorised to chat with me!')

bot.message_loop(handle)
print('I am listening ...')

while 1:
    time.sleep(10)
