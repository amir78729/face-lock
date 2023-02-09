import calendar
import time

from utils.files import get_configs


def log(_msg):
    log_config = get_configs('logging')

    time_stamp = calendar.timegm(time.gmtime())
    log_msg = '{}: {}\n'.format(time_stamp, _msg.upper())

    if log_config['log_in_console']:
        print(log_msg, end='')

    if log_config['log_in_file']:
        with open(log_config['file_path'], 'a') as log_file:
            log_file.write(log_msg)
