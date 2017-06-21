"""
Module to kill windows proccess if after delay check file not contens 1.
Module use config file 'config.json'.
If config file not found then it create.
Config file use json format as:
                     {'FILE_PATH': 'check_connection.txt',
                      'PROCCESS_HOST': '127.0.0.1',
                      'PROCCESS_NAME': 'proccess',
                      'PROCCESS_USER': 'user',
                      'FORCE': False,
                      'DELAY': 0}.
"""
import time
import json
from subprocess import Popen, PIPE

#Default config to create new config file.
DEFAULT_CONFIG = {'FILE_PATH': 'check_connection.txt',
                  'PROCCESS_HOST': '127.0.0.1',
                  'PROCCESS_NAME': 'proccess',
                  'PROCCESS_USER': 'user',
                  'FORCE': False,
                  'DELAY': 0}

def kill_proccess(kill_settings):
    """
    Kill proccess from kill settings. Proccess to kill killed after 10 s.
    Method use taskkill and generate command as:
        'taskkill /F{? if kill_settings['FORCE'] is True}
                  /S {kill_settings['PROCCESS_HOST']} /U {kill_settings['PROCCESS_USER']}
                  /FI "USERNAME eq {kill_settings['PROCCESS_USER']}
                  /IM {kill_settings['PROCCESS_NAME']}"'
    Input:
        kill_settings -> dictionary wit settings to tskkill:
                                {'PROCCESS_HOST': '127.0.0.1',
                                 'PROCCESS_NAME': 'proccess',
                                 'PROCCESS_USER': 'user',
                                 'FORCE': False}
    """
    proccess = Popen(create_taskkill_string(kill_settings),
                     shell=False, stdout=PIPE, stderr=PIPE)
    time.sleep(10)
    proccess.kill()

def create_taskkill_string(kill_settings):
    """
    Create string to taskkill command.
    'taskkill /F{? if kill_settings['FORCE'] is True}
              /S {kill_settings['PROCCESS_HOST']} /U {kill_settings['PROCCESS_USER']}
              /FI "USERNAME eq {kill_settings['PROCCESS_USER']}
              /IM {kill_settings['PROCCESS_NAME']}"'
    Input:
        kill_settings -> dictionary wit settings to tskkill:
                                {'PROCCESS_HOST': '127.0.0.1',
                                 'PROCCESS_NAME': 'proccess',
                                 'PROCCESS_USER': 'user',
                                 'FORCE': False}
    """
    taskkill_string = 'taskkill /F' if kill_settings['FORCE'] else 'taskkill'
    host_string = '/S {}'.format(kill_settings['PROCCESS_HOST'])
    user_string = '/U {user} /FI "USERNAME eq {user}"'.format(user=kill_settings['PROCCESS_USER'])
    proccess_string = '/IM {}'.format(kill_settings['PROCCESS_NAME'])
    return ' '.join([taskkill_string, host_string, user_string, proccess_string])

def check_connection(file_path):
    """
    Check wether the file contains 1.
    Input:
        file_path -> path to check file;
    Output:
        result -> True if check file contains 1 else False;
    """
    with open(file_path) as check_file:
        connection_result = check_file.read(1)
    return True if connection_result == '1' else False

def get_settings():
    """
    Get settings from config file.
    If config file does not exist then create new config file from DEFAULT_CONFIG.
    Output:
        settings -> Dictionary of settings:
                             {'FILE_PATH': 'check_connection.txt',
                              'PROCCESS_HOST': '127.0.0.1',
                              'PROCCESS_NAME': 'proccess',
                              'PROCCESS_USER': 'user',
                              'FORCE': False,
                              'DELAY': 0}.
    """
    with open('config.json', mode='r', encoding='utf-8') as config:
        settings = json.loads(config.read())
    return settings

def create_deffault_config():
    """
    Create default config file from DEFAULT_CONFIG.
    Output:
        DEFAULT_CONFIG -> dictionary of default config:
                                {'FILE_PATH': 'check_connection.txt',
                                 'PROCCESS_HOST': '127.0.0.1',
                                 'PROCCESS_NAME': 'proccess',
                                 'PROCCESS_USER': 'user',
                                 'FORCE': False,
                                 'DELAY': 0}
    """
    with open('config.json', mode='w', encoding='utf-8') as config:
        json.dump(DEFAULT_CONFIG, config)
    return DEFAULT_CONFIG

if __name__ == '__main__':
    try:
        SETTINGS = get_settings()
    except IOError:
        SETTINGS = create_deffault_config()
    time.sleep(SETTINGS['DELAY'])
    if not check_connection(SETTINGS['FILE_PATH']):
        kill_proccess(SETTINGS)
