import configparser
import os

FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
folder_name = "config"
file_name = "config.ini"

PATH = os.path.join(FOLDER_PATH, folder_name)

def create_config() -> None:
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config['General'] = {'language': 'pl', 
                         'model': 'gpt-4.1-mini',
                         'cooldown': 60.0,
                         'minimum_length': 5,
                         'allowed_channels':[]}
    

    # Write the configuration to a file
    with open(os.path.join(PATH, file_name), 'w', encoding="UTF-8") as configfile:
        config.write(configfile)


def read_config() -> dict:
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(os.path.join(PATH, file_name), encoding="UTF-8")

    # Access values from the configuration file
    language = config.get('General', 'language')
    model = config.get('General', 'model')
    cooldown = float(config.get('General','cooldown'))
    minimum_length = int(config.get('General','minimum_length'))
    allowed_channels = __str_to_list(config.get('General','allowed_channels'))
    

    # Return a dictionary with the retrieved values
    config_values = {
        'language': language,
        'model': model,
        'cooldown': cooldown,
        'minimum_length': minimum_length,
        'allowed_channels': allowed_channels
    }

    return config_values


def update_config(language=None, model=None, cooldown=None, minimum_length=None, allowed_channels=[]) -> None:
    config = configparser.ConfigParser()
    config.read(os.path.join(PATH, file_name), encoding="UTF-8")

    if language:
        config.set('General', 'language', language)

    if model:
        config.set('General', 'model', model)

    if cooldown:
        config.set('General', 'cooldown', str(cooldown))
    
    if minimum_length:
        config.set('General', 'minimum_length', str(minimum_length))
    
    if allowed_channels:
        config.set('General', 'allowed_channels', str(allowed_channels))

    with open(os.path.join(PATH, file_name), 'w', encoding="UTF-8") as configfile:
        config.write(configfile)


def __str_to_list(string: str) -> list:
    string = string.strip()
    if not string:
        return []
    
    if string == "[]":
        return []
    
    string = string.replace("[","")
    string = string.replace("]","")
    string = string.replace("'","")
    
    return string.split(",")


if __name__ == "__main__":
    create_config()

    # config_data = read_config()
    # print(config_data['allowed_channels'],type(config_data['allowed_channels']))
    # print("Language: ", config_data['language'])
    # print("Model: ", config_data['model'])

    # update_config(language='en', model='gpt-4.1')
    # config_data = read_config()
    # print("Language: ", config_data['language'])
    # print("Model: ", config_data['model'])