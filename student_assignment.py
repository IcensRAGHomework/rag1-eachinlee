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

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):

    question = question + "請生成一個 JSON 物件，不需要顯示json字串，直接包含一個名為 Result的屬性，先用[]包住該屬性下有兩個子屬性： date :YYYY-MM-DD  和 name :紀念日名稱，只顯示國慶日，，不需顯示任何其他資訊，"
    #print(question)

    response = demo(question)
   
    #json_parser = JsonOutputParser()
    #json_output = json_parser.invoke(response)
    #print(json_output)

    HW01_jstr = response.content

    #print(HW01_jstr)

    Valid_json_data = json.loads(HW01_jstr)

    return HW01_jstr
    

def generate_hw02(question):
    question = question + "請生成一個 JSON 物件，不需要顯示'''json字串，直接包含兩個屬性： year :西元年和 month :月份，不需顯示任何其他資訊，"
    #print(question)
    response = demo(question)
    HW02_jstr = response.content
    #print(HW02_jstr)

    #json.loads() form & Set year & month
    data = json.loads(HW02_jstr)
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

    
def generate_hw03(question2, question3):
    pass
    
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
    #print(HW04_jstr)

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

"""
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
QQ4="請問日本隊的積分是多少"
print(QQ4)
RR = generate_hw04(QQ4)
#"""

#RR = demo(QQ)
#print(RR.content)