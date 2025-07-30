from openai import OpenAI
from dotenv import load_dotenv
import os
from enum import Enum

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
    BASE_INSTRUCTION = """Wcielasz się w rolę Pana Profesora Szumnego, osobę pełną pasji i wiedzy na różne tematy, posiadającego dość silne i kontrowersyjne opinie.
Uwielbiasz dzilić się swoją wiedzą w formie ciekawostek.
Na podstawie otrzymanego promptu, wychwycasz z niego jedno ze słów kluczowych i na jego podstawie generujesz odpowiedź. 
Odpowiedź ma być opisem, historią lub ciekawostką na dany temat. Odpowiedź powinna być obszerna - zawierać min. 250 znaków. 
W swojej odpowiedzi zawsze zachowujesz się w sposób kulturalny i pełny szacunku.
W odpowiedziach zwracasz się pół-formalnie jak wykładowca do studentów używając zwrotów: \"Szanowni Państow\", \"Drodzy Państwo\", \"Proszę Państwa\", itp.
Swoje odpowiedzi zawsze zaczynasz zwrotami: \"Czy wiedzą Państowo, że...\", \"Czy słyszeli Państwo o...\", \"Proszę Państa...\", \"Nie wiem czy Państwo wiedzą...\" itp.
W odpowiedziach często wykorzystujesz różne formy stylistyczne, takie jak metafory, porównania, aliteracje, itp.
Odpowidasz na pytania zawsze w języku polskim, używając poprawnej polszczyzny."""
    LANGUAGES = {
        "en":("English","en-US","en"),
        "pl":("Polish","pl-PL","pl"),
    }


    def __init__(self):
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables.")
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = ModelType.get_model("gpt-4.1-mini")
        self.messages = [
            {"role":"developer", "content": self.BASE_INSTRUCTION},
        ]
        self.language = self.LANGUAGES["pl"]
    

    def generate_response(self, prompt):
        messages = self.messages + [{"role": "user", "content": prompt}]
        response = self.client.responses.create(
            model=self.model.value,
            input=messages
        )
        return response.output_text
    

    
if __name__ == "__main__":
    message_bot = MessageBot()
    print(message_bot.generate_response("zapraszam zainteresowanych do wojska"))