import sys
sys.path.append(".")

import logging
from enum import Enum

from openai import OpenAI
from openai.types.chat import ChatCompletion

from config import OPENAI_API_KEY


logger = logging.getLogger(__name__)


class GPTModelEnum(Enum):
    GPT_4O = "gpt-4o"
    GPT_4_TURBO = "gpt-4-turbo"
    GPT_4 = "gpt-4"
    GPT_3_5_TURBO = "gpt-3.5-turbo"


class GPTChatRoleEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


class ChatGPTHelper:
    def __init__(self):
        try:
            super().__init__()
            self.client = OpenAI(api_key=OPENAI_API_KEY)
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception("OpenAI client error")

    def chat(
        self,
        user_input: str,
        system_setting: str,
        model: str =GPTModelEnum.GPT_3_5_TURBO.value
    ) -> str:
        messages = [
            {
                "role": GPTChatRoleEnum.USER.value,
                "content": user_input
            },
            {
                "role": GPTChatRoleEnum.SYSTEM.value,
                "content": system_setting
            }
        ]
        
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            n=1,
        )

        return self.convert_gpt_response(response)
        
        
    def convert_gpt_response(self, gpt_response: ChatCompletion):
        result_list = [
            choice.message.content
            for choice in gpt_response.choices
        ]
        
        return "".join(result_list)
