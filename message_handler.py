from message_engine import MessageBot
from langdetect import detect_langs, detect
from translator import Translator
from datetime import datetime, timedelta
from random import choice
from config import update_config, read_config


class MesssageHandler:
    last_message_time = datetime.now()
    is_ready_to_respond = True
    
    def __init__(self, translator: Translator = None) -> None:
        self.translator = translator or Translator(locale_folder='localization', default_language='pl')
        self.message_bot = MessageBot(translator=self.translator)

        self.message_cooldown = read_config().get('cooldown', 60)
        self.minimum_message_length = read_config().get('minimum_length',5)
        self.allowed_channels:list = read_config().get('allowed_channels',[])
    
    
    async def change_language(self, language) -> None:
        self.message_bot.change_language(language)


    async def is_message_language_supported(self, message) -> bool:
        #lang, _ = classify(message.content)
        lang = detect(message.content)
        langs = detect_langs(message.content)
        print(langs, lang, sep=" / ")
        if lang not in self.message_bot.language:
            return False
        return True

    def is_word_language_supported(self, word) -> bool:
        lang = detect(word)
        langs = detect_langs(word)
        print(langs, lang, sep=" / ")
        if lang not in self.message_bot.language:
            return False
        return True


    def is_word_in_current_language(self, word) -> bool:
        lang = detect(word)
        if lang != self.translator.default_language:
            return False
        return True


    async def can_respond(self) -> bool:
        self.update_cooldown()
        if self.is_ready_to_respond:
            self.is_ready_to_respond = False
            self.last_message_time = datetime.now()
            return True
        return False


    def update_cooldown(self) -> None:
        if self.last_message_time + timedelta(seconds=self.message_cooldown) < datetime.now():
            self.is_ready_to_respond = True
            self.last_message_time = datetime.now()


    async def generate_response(self, message) -> str:
        response = f"debug: {message.content}\n{message.created_at}"  # For debugging purposes, replace with actual response generation
        #response = self.message_bot.generate_response(message.content)
        return response


    def is_real_word(self, word, language) -> bool:
        lang_code = self.translator.languages["codes"].get(language, language)
        if self.translator.enchant_dict.get(lang_code) is None:
            return False
        return self.translator.enchant_dict[lang_code].check(word)
    
    
    async def is_message_length_valid(self, message) -> bool:
        words = message.content.split(" ")
        if len(words) < self.minimum_message_length:
            return False
        return True

    
    async def set_minimum_message_length(self, length: int) -> None:
        if length < 1:
            raise ValueError(self.translator.message_handler['min_message_length_invalid'])
        self.minimum_message_length = length
        update_config(minimum_length=self.minimum_message_length)


    async def set_message_cooldown(self, cooldown: float) -> None:
        if cooldown < 0.1:
            raise ValueError(self.translator.message_handler['cooldown_invalid'])
        self.message_cooldown = cooldown
        update_config(cooldown=self.message_cooldown)


    async def add_allowed_channel(self, channel_name: str) -> None:
        if not channel_name:
            raise ValueError(self.translator.message_handler['invalid_channel_name'])
        
        if channel_name in self.allowed_channels:
            raise ValueError(self.translator.message_handler['channel_already_allowed'].format(channel=channel_name))
        
        self.allowed_channels.append(channel_name)
        update_config(allowed_channels=self.allowed_channels)


    async def remove_allowed_channel(self, channel_name: str) -> None:
        if not channel_name:
            raise ValueError(self.translator.message_handler['invalid_channel_name'])
        
        if channel_name not in self.allowed_channels:
            raise ValueError(self.translator.message_handler['channel_not_allowed'].format(channel=channel_name))
        
        self.allowed_channels.remove(channel_name)
        update_config(allowed_channels=self.allowed_channels)


    async def clear_allowed_channels(self) -> None:
        self.allowed_channels.clear()
        update_config(allowed_channels=self.allowed_channels)
    

    async def get_allowed_channels(self) -> list:
        return self.allowed_channels


    async def is_channel_allowed(self, channel_name: str) -> bool:
        if channel_name in self.allowed_channels:
            return True
        return False


    async def handle_unknown_message(self, message) -> str:
        words = message.content.split()
        lang = detect(message.content)
        appropriate_words = []
        for word in words:
            if self.is_word_in_current_language(word):
                print(f"Skipping unsupported word: {word}")
                continue

            if len(word) < 5:
                print(f"Skipping short word: {word}")
                continue

            if not self.is_real_word(word, lang):
                print(f"Skipping non-real word: {word}")
                continue
            
            appropriate_words.append(word)
            
        if appropriate_words:
            word = choice(appropriate_words)
            response = self.handle_unknown_word(word)
            return response

        return None


    def handle_unknown_word(self, word) -> str:
        response = f"Hmm, I don't know the word '{word}'. I'll have to check it out later!"
        return response
    
    
    async def change_model(self, model_name) -> None:
        try:
            self.message_bot.change_model(model_name)
        except ValueError as err:
            raise ValueError(self.translator.message_handler['model_not_supported'].format(model=model_name))