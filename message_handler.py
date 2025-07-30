from message_engine import MessageBot
from langid import classify
from translator import Translator

class MesssageHandler:
    message_cooldown = 5.0  # in seconds
    
    
    def __init__(self, translator: Translator = None):
        self.translator = translator or Translator(locale_folder='localization', default_language='pl')
        self.message_bot = MessageBot(translator=self.translator)
    
    
    async def is_message_language_supported(self, message):
        lang, _ = classify(message.content)
        if lang not in self.message_bot.language:
            return False
        return True


    async def handle_message(self, message):
        response = self.message_bot.generate_response(message.content)

        return response
    

