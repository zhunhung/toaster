import os, requests
import datetime
import json

from toaster.helper import get_config_path, load_config, format_time

CONFIG = load_config()

def telegram_toast(method):
    API_ENDPOINT = 'https://us-central1-toaster-253815.cloudfunctions.net/toaster_message'

    # Check for telegram config
    if 'telegram' not in CONFIG.keys():
        raise UnboundLocalError("You have not configured your Telegram ID. Run set_config(<telegram id>, 'telegram') first.")

    def insert_toast(*args, **kw):
        try:
            start = datetime.datetime.now()
            result = method(*args, **kw)
            end = datetime.datetime.now()
            diff = end - start
            # Create Message
            msg = "🍞 Ding! Function <i>{}</i> has completed!\n<b>Start Time:</b> {}\n<b>End Time:</b> {}\n<b>Time Taken:</b> {}".format(
                method.__name__, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), format_time(diff)
            )
            data = {
                'userid':CONFIG['telegram'],
                'msg':msg
            }

            res = requests.post(url = API_ENDPOINT, data = data)
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function <i>{}</i>\n<b>Error message:</b> {}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'userid':CONFIG['telegram'],
                'msg':msg
            }
            # Send Telegram Message
            res = requests.post(url = API_ENDPOINT, data = data)

    return insert_toast

def slack_toast(method):
    # Check for telegram config
    if 'slack' not in CONFIG.keys():
        raise UnboundLocalError("You have not configured your Slack Webhook Url. Run set_config(<slack webhook url>, 'slack') first.")

    def insert_toast(*args, **kw):
        try:
            start = datetime.datetime.now()
            result = method(*args, **kw)
            end = datetime.datetime.now()
            diff = end - start
            # Create Message
            msg = "🍞 Ding! Function *{}* has completed!\n*Start Time:* {}\n*End Time:* {}\n*Time Taken:* {}".format(
                method.__name__, start.strftime("%Y-%m-%d %H:%M:%S"), end.strftime("%Y-%m-%d %H:%M:%S"), format_time(diff)
            )
            data = {
                'text':msg
            }

            res = requests.post(url = CONFIG['slack'], data = json.dumps(data), headers={'Content-Type': "application/json"})
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function *Error message:* {}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'text':msg
            }
            # Send Telegram Message
            res = requests.post(url = CONFIG['slack'], data = data, headers={'Content-Type': "application/json"})

    return insert_toast


def set_config(config_str, notification_channel):
    config_str = str(config_str)
    notification_channel = str(notification_channel)

    # Check for valid config_str
    if notification_channel == 'telegram':
        if not config_str.isnumeric():
            raise TypeError('Your Telegram ID should be all numbers.')

    elif notification_channel == 'slack':
        if 'slack.com' not in config_str:
            raise ValueError('Ensure that you enter a valid incoming webhook')
    else:
        raise ValueError('Invalid method, enter either `telegram` or `slack`')

    # Load and save to config.json
    global CONFIG
    CONFIG[notification_channel] = config_str
    config_path = get_config_path()
    with open(config_path,"w") as config_file:
        json.dump(CONFIG, config_file)
