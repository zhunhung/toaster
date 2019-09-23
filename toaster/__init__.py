import os, requests
import datetime

from toaster.helper import get_config_path, load_default_id, format_time

USERID = load_default_id()
API_ENDPOINT = 'https://us-central1-toaster-253815.cloudfunctions.net/toaster_message'

def toast(method):
    if USERID == '':
        raise UnboundLocalError('You have not configured your Telegram ID. Run set_id(<telegram id>) first.')

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
                'userid':USERID,
                'msg':msg
            }

            res = requests.post(url = API_ENDPOINT, data = data)
            return result

        except Exception as e:
            msg = '⚠️ An error has occurred with function <i>{}</i>\n<b>Error message:</b> {}'.format(method.__name__, str(e))
            print('Error caught:',e)
            data = {
                'userid':USERID,
                'msg':msg
            }
            # Send Telegram Message
            res = requests.post(url = API_ENDPOINT, data = data)

    return insert_toast

def set_id(userid):
    userid = str(userid)
    if userid.isnumeric():
        config_path = get_config_path()
        with open(config_path,"w") as config_file:
            config_file.write(userid)
        global USERID
        USERID = userid
    else:
        raise TypeError('Your Telegram ID should be all numbers.')



