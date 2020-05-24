import configparser



def read_config():

    ## Read Config
    config = configparser.ConfigParser()
    config.sections()
    config.read('settings.cfg')

    return config


def save_config(config):
    
    ## Save the config file
    with open('settings.cfg', 'w') as f:
        config.write(f)


def update_config(config, section, key, value):
    
    ## Change the value of a key
    config.set(section, key, value)
    save_config(config)

def get_config_value(config, section, key):
    
    ## Change the value of a key
    return config.get(section, key)
