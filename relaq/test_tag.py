import pandas as pd
from chatgpt.constants import TAG_PROMPT
from chatgpt.services import ChatGPTHelper, GPTModelEnum

df = pd.read_excel("[大安區 美甲]AI_Summary_20250223184254.xlsx")

chatgpt_helper = ChatGPTHelper()

result = []


for index, row in df.iterrows():
    print(f"processing . . . {index}")
    
    ai_result = chatgpt_helper.chat(
        user_input=f"""
        店家基本資訊:{row["店家資訊"]},
        店家評論:{row["店家評論"]},
        店家價格與服務:{row["店家價格與服務"]},
        """,
        system_setting=TAG_PROMPT,
        model=GPTModelEnum.GPT_4O_MINI.value,
    )

    result.append({
        "店家資訊": row["店家資訊"],
        "店家評論": row["店家評論"],
        "店家價格與服務": row["店家價格與服務"],
        "AI_summary": ai_result
    })
        

output_df = pd.DataFrame(result)

output_df.to_excel("test_tag.xlsx", index=False)

    
    



