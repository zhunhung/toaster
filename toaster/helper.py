import os

def get_config_path():
    current_dir = __file__
    parent_dir = os.path.dirname(current_dir)
    config_path = os.path.join(parent_dir, 'config.txt')
    return config_path

def load_default_id():
    userid = ''
    config_path = get_config_path()
    if os.path.isfile(config_path):
        with open(config_path,"r") as config_file:
            userid = config_file.readlines()
    return userid

def format_time(time_diff):
    days = time_diff.days
    hours, remainder = divmod(time_diff.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if days > 0:
        return '{} days, {} hours, {} mins, {} sec'.format(days, int(hours), int(minutes), seconds)
    return '{} hours, {} mins, {} sec'.format(int(hours), int(minutes), seconds)