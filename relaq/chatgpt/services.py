import logging
from enum import Enum

from django.conf import settings
from openai import OpenAI
from openai.types.chat import ChatCompletion


logger = logging.getLogger(__name__)


class GPTModelEnum(Enum):
    GPT_4O = "gpt-4o"
    GPT_4O_MINI = "gpt-4o-mini"
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
            self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            logger.info(e, exc_info=True)
            raise Exception("OpenAI client error")

    def chat(
        self,
        user_input: str,
        system_setting: str,
        model: str =GPTModelEnum.GPT_4O_MINI.value
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

    def convert_tag_response(self, gpt_response: str) -> list[dict]:
        """將 GPT 的標籤回應轉換為資料庫格式
        
        Args:
            gpt_response: GPT 回傳的標籤文字
            
        Returns:
            list[dict]: 轉換後的標籤列表，每個標籤包含 name, type, emoji, description
        """
        tags = []
        current_type = None
        
        # 處理多個店家的分隔
        responses = gpt_response.split('======')
        for response in responses:
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # 處理類型標題
                if '一、' in line:
                    current_type = 'STYLE'
                elif '二、' in line:
                    current_type = 'TECHNIQUE'
                elif '三、' in line:
                    current_type = 'PRICE'
                elif '四、' in line:
                    current_type = 'ENVIRONMENT'
                elif '五、' in line:
                    current_type = 'TRANSPORTATION'
                elif '六、' in line:
                    current_type = 'TARGET_AUDIENCE'
                # 處理標籤內容
                elif current_type and ('：' in line or ':' in line):
                    try:
                        # 分割 emoji、名稱和描述
                        parts = line.split('：' if '：' in line else ':')
                        if len(parts) == 2:
                            name_with_emoji = parts[0].strip()
                            description = parts[1].strip()
                            
                            # 找出 emoji（通常是第一個字元組）
                            words = name_with_emoji.split()
                            if len(words) >= 2:
                                emoji = words[0].strip()
                                name = ' '.join(words[1:]).strip()
                                
                                if emoji and name:  # 確保都有值
                                    tags.append({
                                        'name': name,
                                        'type': current_type,
                                        'emoji': emoji,
                                        'description': description
                                    })
                    except Exception as e:
                        logger.warning(f"解析標籤失敗: {line}, 錯誤: {str(e)}")
                        continue
        
        return tags