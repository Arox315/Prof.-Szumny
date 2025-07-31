import json
import os


class Translator:
    def __init__(self, locale_folder='localization', default_language='pl'):
        self.locale_folder = locale_folder
        self.default_language = default_language
        self.translations = {}
        self.load_translations()
        self.set_translations()
    

    def load_translations(self):
        for filename in os.listdir(self.locale_folder):
            if filename.endswith('.json'):
                language_code = filename.replace('.json', '')
                with open(os.path.join(self.locale_folder, filename), 'r', encoding='utf-8') as file:
                    self.translations[language_code] = json.load(file)
    
    
    async def set_language(self, language_code):
        if language_code in self.translations:
            self.default_language = language_code
            self.set_translations()
        else:
            if language_code not in self.languages.keys():
                raise ValueError(self.translator['language_not_supported'].format(language=language_code))
            else:
                raise ValueError(self.translator['language_not_supported'].format(language=self.languages[language_code]))

    
    def set_message_bot_translations(self):
        self.message_bot = self.translations[self.default_language]["translation"].get('message_bot', {})

    
    def set_messgage_handler_translations(self):
        self.message_handler = self.translations[self.default_language]["translation"].get('message_handler', {})


    def set_languages_translations(self):
        self.languages = self.translations[self.default_language]["translation"].get('languages', {})


    def set_translator_translations(self):
        self.translator = self.translations[self.default_language]["translation"].get('translator', {})


    def set_discord_translations(self):
        self.discord = self.translations[self.default_language]["translation"].get('discord', {})


    def set_translations(self):
        self.set_message_bot_translations()
        self.set_messgage_handler_translations()
        self.set_languages_translations()
        self.set_translator_translations()
        self.set_discord_translations()


if __name__ == "__main__":
    # Example usage
    t = Translator()
    print(t.message_bot["base_instruction"])