import json
import os
import enchant

class Translator:
    enchant_dict: dict = {}
    def __init__(self, locale_folder='localization', default_language='pl'):
        self.locale_folder = locale_folder
        self.default_language = default_language
        #self.set_default_language_dict_code()
        #self.enchant_dict = enchant.Dict(self.default_language_dict_code)  # Default to English dictionary
        self.set_enchant_dict()
        self.translations = {}
        self.load_translations()
        self.set_translations()

        self.default_language_dict_code = self.languages["codes"].get(self.default_language, self.default_language)
   

    def load_translations(self):
        for filename in os.listdir(self.locale_folder):
            if filename.endswith('.json'):
                language_code = filename.replace('.json', '')
                with open(os.path.join(self.locale_folder, filename), 'r', encoding='utf-8') as file:
                    self.translations[language_code] = json.load(file)
    
    
    async def set_language(self, language_code):
        if language_code in self.translations:
            self.default_language = language_code
            self.default_language_dict_code = self.languages["codes"].get(self.default_language, self.default_language)
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


    def set_enchant_dict(self):
        for lang in enchant.list_languages():
            self.enchant_dict[lang] = enchant.Dict(lang)


if __name__ == "__main__":
    # Example usage
    t = Translator()
    #print(t.message_bot["base_instruction"])
    #print(enchant.list_languages(),enchant.dict_exists("en_US"), enchant.dict_exists("pl_PL"))


    d = enchant.Dict("en_US")
    print(d.check("hello"))
    print(d.check("intend"))