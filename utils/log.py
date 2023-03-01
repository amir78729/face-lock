import time
import calendar

from utils.files import get_configs
from colorama import *


def log(_msg):
    log_config = get_configs('logging')

    time_stamp = calendar.timegm(time.gmtime())
    log_msg = '{}: {}\n'.format(time_stamp, _msg.upper())

    if log_config['log_in_console']:
        print(Fore.CYAN + log_msg.split(':', 1)[0] + Fore.RESET + log_msg.split(':', 1)[1], end='')

    if log_config['log_in_file']:
        with open(log_config['file_path'], 'a') as log_file:
            log_file.write(log_msg)
