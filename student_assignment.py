import json
import traceback
import re
import requests
import base64
import os


from model_configurations import get_model_configuration
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

from typing import List
from pydantic import BaseModel, Field
from langchain.memory import ConversationBufferMemory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
store = {}

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def setllm():

    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )

    return llm


def generate_hw01(question):

    prompt_template = """ Please generate a JSON object format. Please do not need to display the '''json string. The direct output format is as follows example
    {
        "Result": [
            {
                "date": "2024-10-10",
                "name": "國慶日"
            }
        ]
    }
    """

    llm = setllm()

    messages=[
            { "role": "system", "content": prompt_template },
            { "role": "user", "content": [
                { "type": "text", "text": question },
            ] }
            ]

    response = llm.invoke(messages)

    HW01_jstr = response.content

    #print(HW01_jstr)

    Valid_json_data = json.loads(HW01_jstr)

    return HW01_jstr
    

def generate_hw02(question):

    prompt_template = """ Please get Year & month from message and generate a JSON object format. Please do not need to display the '''json string. The direct output format is as follows example
    {
        "year": "YYYY",
        "month": "MM"
    }
    """
    llm = setllm()

    messages=[
            { "role": "system", "content": prompt_template },
            { "role": "user", "content": [
                { "type": "text", "text": question },
            ] }
            ]

    response = llm.invoke(messages)

    HW02_jstr = response.content
    #print(HW02_jstr)

    #json.loads() form & Set year & month
    data = json.loads(HW02_jstr)
    #print(data)

    year = data['year']
    month = data['month']
    #print(f"年份: {year}")
    #print(f"月份: {month}")

    #set Calendarific API Key & country
    api_key = "sBWjJUOnRNi26kc6d9w3HYlWSsLW9gy8"
    country = "TW"

    #set Calendarific API Requset
    url = f"https://calendarific.com/api/v2/holidays?api_key={api_key}&country={country}&year={year}&month={month}"

    #send Req to Calendarific
    response = requests.get(url)
    data = response.json()

    #handle Response Data to json
    result_json_string = []
    for holiday in data['response']['holidays']:
        result_json_string.append({
            "date": holiday['date']['iso'],
            "name": holiday['name']
        })

    #json dump format
    result_json_string = json.dumps({"Result": result_json_string}, ensure_ascii=False, indent=4)

    #print(result_json_string)
    
    return result_json_string

# Ref https://python.langchain.com/docs/how_to/agent_executor/
class InMemoryHistory(BaseChatMessageHistory, BaseModel):
    """In memory implementation of chat message history."""

    messages: List[BaseMessage] = Field(default_factory=list)

    def add_messages(self, messages: List[BaseMessage]) -> None:
        """Add a list of messages to the store"""
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages = []
    
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryHistory()
    return store[session_id]
    
def generate_hw03(question2, question3):

    prompt_template = """ Please generate a JSON object format. Please do not need to display the '''json string. The direct output format is as follows example
    {
        "Result": [
            {
                "date": "YYYY-MM-DD",
                "name": "Day Name"
            }
        ]
    }
    """

    llm = setllm()

    Q2C_Str = "請幫我翻譯，並記得這這節日清單Name的中文" + generate_hw02(question2)

    messages=[
            { "role": "system", "content": prompt_template },
            { "role": "user", "content": [
                { "type": "text", "text": Q2C_Str },
            ] }
            ]

    response = llm.invoke(messages)

    holiday_list_JStr = response.content
    print(holiday_list_JStr)

    Valid_json_data = json.loads(holiday_list_JStr)

    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ 
    print("======================================================")
    #Ref CH4 Page 4-6
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Checks whether a holiday is included in the list of holidays for that month, and responds whether the holiday needs to be added or not"),
        ("ai", "{holiday_list}"),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ])

    chain = prompt | llm

    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="history",
    )

    res_check_holiday = chain_with_history.invoke(
        {"holiday_list": Valid_json_data, 
         "question": question3},
        config={"configurable": {"session_id": "HW3"}}
    )
    print(res_check_holiday.content)

    prompt_final = """ 請幫忙根據前面結果，輸出一個JSON物件，do not need to display the '''json string，結果Result包含
    add : 這是一個布林值，表示是否需要將節日新增到節日清單中。根據問題判斷該節日是否存在於清單中，如果不存在，則為 true；否則為 false。
    reason : 描述為什麼需要或不需要新增節日，具體說明是否該節日已經存在於清單中，以及若需要將節日新增到節日清單中，增加後清單的內容。
    整個 JSON 格式範例範例如下：
    {
    "Result": 
        {
            "add": true,
            "reason": "蔣中正誕辰紀念日並未包含在十月的節日清單中。目前十月的現有節日包括國慶日、重陽節、華僑節、台灣光復節和萬聖節。因此，如果該日被認定為節日，應該將其新增至清單中。"
        }
    }
    """
    res_final_result = chain_with_history.invoke(
        {"holiday_list": Valid_json_data, 
         "question": prompt_final},
        config={"configurable": {"session_id": "HW3"}}
    )
    print(res_final_result.content)
    
    HW03_jstr = res_final_result.content

    return HW03_jstr
    
def generate_hw04(question):

    # 1. 讀取圖片並轉換為 Base64 編碼
    filename = "baseball.png"
    current_directory = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_directory, filename)

    # 檢查圖片檔案是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"檔案 {filename} 不存在於目錄 {current_directory}")

    # 讀取圖片並將其轉換為 Base64 編碼
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded = base64.b64encode(image_data).decode('utf-8')

    # 生成 Data URL（假設圖片是 PNG 格式）
    data_url = f"data:image/png;base64,{base64_encoded}"

    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    prompt_template = """ 請生成一個 JSON 物件格式，不需要顯示'''json字串，直接(不要加```json):
     {
         "Result":
             {
                 "score": 0000
             }
     }
    """
    messages=[
            { "role": "system", "content": prompt_template },
            { "role": "user", "content": [
                { "type": "text", "text": question },
                { "type": "image_url", "image_url": {"url": data_url } }
            ] }
            ]

    response = llm.invoke(messages)
    #print(prompt_str)

    HW04_jstr = response.content
    print(HW04_jstr)

    return HW04_jstr

    
def demo(question):

    llm = AzureChatOpenAI(
            model=gpt_config['model_name'],
            deployment_name=gpt_config['deployment_name'],
            openai_api_key=gpt_config['api_key'],
            openai_api_version=gpt_config['api_version'],
            azure_endpoint=gpt_config['api_base'],
            temperature=gpt_config['temperature']
    )
    message = HumanMessage(
            content=[
                {"type": "text", "text": question},
            ]
    )
    response = llm.invoke([message])

    #print(response.content)

    return response



"""
#Test generate_hw01
print("generate_hw01 請回答台灣特定月份的紀念日有哪些(請用JSON格式呈現)?")
QQ="2024年台灣10月紀念日有哪些?"
print(QQ)
RR = generate_hw01(QQ)
#"""

"""
#Test generate_hw02
print("generate_hw02 請回答台灣特定月份的紀念日有哪些(請用API Call)?")
QQ="2024年台灣10月紀念日有哪些?"
print(QQ)
RR = generate_hw02(QQ)
#"""

#"""
#Test generate_hw03
print("generate_hw03 請回答?")
QQ2="2024年台灣10月紀念日有哪些?"
QQ3='''根據先前的節日清單，這個節日{"date": "10-31", "name": "蔣公誕辰紀念日"}是否有在該月份清單？'''
print(QQ2)
print(QQ3)
RR = generate_hw03(QQ2,QQ3)
#"""

"""
#Test generate_hw04
print("generate_hw04 請回答?")
QQ4="請問USA的積分是多少"
print(QQ4)
RR = generate_hw04(QQ4)
#"""

#RR = demo(QQ)
#print(RR.content)