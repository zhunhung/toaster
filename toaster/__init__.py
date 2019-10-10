import os, requests
import datetime

from toaster.helper import get_config_path, load_default_id, format_time

webhook_url = load_default_id()

def toast(method):
    if webhook_url == '':
        raise UnboundLocalError('You have not configured your Telegram ID. Run set_incoming_webhook(<telegram id>) first.')

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
                'text':msg
            }

            res = requests.post(url = WEBHOOK_URL, data = data, headers={'Content-Type': "application/json"})
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function <i>{}</i>\n<b>Error message:</b> {}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'text':msg
            }
            # Send Telegram Message
            res = requests.post(url = WEBHOOK_URL, data = data, headers={'Content-Type': "application/json"})

    return insert_toast

def set_incoming_webhook(webhook_url):
    webhook_url = str(webhook_url)
    config_path = get_config_path()
    with open(config_path,"w") as config_file:
        config_file.write(webhook_url)
    global WEBHOOK_URL
    WEBHOOK_URL = webhook_url
