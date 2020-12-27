from configparser import SafeConfigParser
import atexit

config = SafeConfigParser()
config.read('config.ini')

def getconfig():
    global config
    print('Requested config...')
    return config

def saveconfig():
    global config
    with open('config.ini', 'w') as configfile:    # save
        print('Saving changes before exiting the program...')
        try:
            config.write(configfile)
            print('Success!')
        except Exception as e:
            print('An unexpected error occurred when trying to save the config. {}'.format(e))

atexit.register(saveconfig)