from message_engine import MessageBot
from langid import classify

class MesssageHandler:
    message_cooldown = 5.0  # in seconds
    message_bot = MessageBot()
    
    def __init__(self):
        pass

    
    # async def change_language(self, language):
    #     if language not in self.message_bot.LANGUAGES.keys():
    #         raise ValueError(f"Language {language} is not supported.")
    #     self.message_bot.language = self.message_bot.LANGUAGES[language]
    #     return f"Language changed to {self.message_bot.language[0]}."


    async def is_message_language_supported(self, message):
        lang, _ = classify(message.content)
        if lang not in self.message_bot.language:
            return False
        return True


    async def handle_message(self, message):
        response = self.message_bot.generate_response(message.content)

        return response
    


    