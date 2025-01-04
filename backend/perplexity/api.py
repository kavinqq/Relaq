import sys
sys.path.append(".")

import logging

from openai import OpenAI
from openai.types.chat import ChatCompletion

from config import PERPLEXITY_API_KEY


logger = logging.getLogger(__name__)


class PerplexityHelper:
    def __init__(self):
        try:
            super().__init__()
            self.client = OpenAI(
                api_key=PERPLEXITY_API_KEY,
                base_url="https://api.perplexity.ai"
            )
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception("Perplexity client error")

    def get_resp(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-sonar-large-128k-online",
                messages=[
                    {
                        "role": "system",
                        "content": "請針對台灣的美甲店資訊去搜尋"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )
            
            for res in response:
                print(res)            
            return self.convert_gpt_response(response)
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception("Perplexity error")

    
    def convert_gpt_response(self, gpt_response: ChatCompletion):
        result_list = [
            choice.message.content
            for choice in gpt_response.choices
        ]
        
        return "".join(result_list)
