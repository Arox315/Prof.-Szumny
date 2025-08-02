import configparser
import os

FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
folder_name = "config"
file_name = "config.ini"

PATH = os.path.join(FOLDER_PATH, folder_name)

def create_config():
    config = configparser.ConfigParser()

    # Add sections and key-value pairs
    config['General'] = {'language': 'pl', 'model': 'gpt-4.1-mini'}
    

    # Write the configuration to a file
    with open(os.path.join(PATH, file_name), 'w') as configfile:
        config.write(configfile)


def read_config():
    # Create a ConfigParser object
    config = configparser.ConfigParser()

    # Read the configuration file
    config.read(os.path.join(PATH, file_name))

    # Access values from the configuration file
    language = config.get('General', 'language')
    model = config.get('General', 'model')
    

    # Return a dictionary with the retrieved values
    config_values = {
        'language': language,
        'model': model
    }

    return config_values


def update_config(language=None, model=None):
    config = configparser.ConfigParser()
    config.read(os.path.join(PATH, file_name))

    if language:
        config.set('General', 'language', language)
    if model:
        config.set('General', 'model', model)

    with open(os.path.join(PATH, file_name), 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    create_config()

    # config_data = read_config()
    # print("Language: ", config_data['language'])
    # print("Model: ", config_data['model'])

    # update_config(language='en', model='gpt-4.1')
    # config_data = read_config()
    # print("Language: ", config_data['language'])
    # print("Model: ", config_data['model'])