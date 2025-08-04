from openai import OpenAI
from dotenv import load_dotenv
import os
from enum import Enum
from translator import Translator
from config import update_config, read_config

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class ModelType(Enum):
    GPT_4_1 = "gpt-4.1"
    GPT_4_1_MINI = "gpt-4.1-mini"
    GPT_4o = "gpt-4o"
    GPT_4o_MINI = "gpt-4o-mini"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


    @classmethod
    def get_model(cls, model_name):
        for model in cls:
            if model.value == model_name:
                return model
        raise ValueError(f"Model {model_name} not found.")


    @classmethod
    def get_all_models(cls):
        return [model.value for model in cls]


class MessageBot:
    def __init__(self,translator: Translator = None):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        
        default_language = read_config().get('language', 'pl')
        model = read_config().get('model', 'gpt-4.1-mini')

        self.translator = translator or Translator(locale_folder='localization', default_language=default_language)
        self.base_instruction = self.translator.message_bot['base_instruction']
        self.languages = self.translator.translations.keys()

        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = ModelType.get_model(model)
        self.messages = [
            {"role":"developer", "content": self.base_instruction},
        ]

        self.language = self.translator.default_language
    

    def generate_response(self, prompt):
        messages = self.messages + [{"role": "user", "content": prompt}]
        response = self.client.responses.create(
            model=self.model.value,
            input=messages
        )
        return response.output_text
    

    def change_language(self, language):
        if language not in self.languages:
            raise ValueError(self.translator.message_handler['language_not_supported'].format(language=self.translator.languages[language]))
        self.language = language
        update_config(language=language)
        self.messages[0]["content"] = self.base_instruction


    def change_model(self, model_name):
        try:
            self.model = ModelType.get_model(model_name)
            update_config(model=model_name)
            self.messages[0]["content"] = self.base_instruction
        except ValueError as err:
            raise ValueError(self.translator.message_handler['model_not_supported'].format(model=model_name))


if __name__ == "__main__":
    message_bot = MessageBot()
    print(message_bot.generate_response("zapraszam zainteresowanych do wojska"))