from message_engine import MessageBot
from langdetect import detect_langs, detect
from translator import Translator
from datetime import datetime, timedelta
import test_t


class MesssageHandler:
    message_cooldown = 10.0  # in seconds
    last_message_time = datetime.now()
    is_ready_to_respond = True
    
    def __init__(self, translator: Translator = None):
        self.translator = translator or Translator(locale_folder='localization', default_language='pl')
        self.message_bot = MessageBot(translator=self.translator)
    
    
    async def change_language(self, language):
        self.message_bot.change_language(language)


    async def is_message_language_supported(self, message):
        #lang, _ = classify(message.content)
        lang = detect(message.content)
        langs = detect_langs(message.content)
        print(langs, lang, sep=" / ")
        if lang not in self.message_bot.language:
            return False
        return True


    async def handle_message(self, message):
        # Check if the bot is ready to respond based on cooldown
        if self.is_ready_to_respond:
            self.is_ready_to_respond = False
            self.last_message_time = datetime.now()
            return self.generate_response(message)
        
        # Check if enough time has passed since the last message and update the state
        if self.last_message_time + timedelta(seconds=self.message_cooldown) < datetime.now():
            self.is_ready_to_respond = True
            self.last_message_time = datetime.now()
            #return self.generate_response(message)

        return None
    

    async def can_respond(self) -> bool:
        self.update_cooldown()
        if self.is_ready_to_respond:
            self.is_ready_to_respond = False
            self.last_message_time = datetime.now()
            return True
        return False
        
    
    def update_cooldown(self):
        if self.last_message_time + timedelta(seconds=self.message_cooldown) < datetime.now():
            self.is_ready_to_respond = True
            self.last_message_time = datetime.now()


    async def generate_response(self, message):
        response = f"debug: {message.content}\n{message.created_at}"  # For debugging purposes, replace with actual response generation
        #response = self.message_bot.generate_response(message.content)
        return response