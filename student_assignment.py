import json
import traceback
import re
import requests
import base64
import os
from PIL import Image

from langchain.chat_models import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from mimetypes import guess_type
from model_configurations import get_model_configuration
from pytesseract import image_to_string


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
    pass
    
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





#"""
#Test generate_hw01
print("generate_hw01 請回答台灣特定月份的紀念日有哪些(請用JSON格式呈現)?")
QQ="2024年台灣10月紀念日有哪些?"
print(QQ)
RR = generate_hw01(QQ)
#"""

#"""
#Test generate_hw01
print("generate_hw02 請回答台灣特定月份的紀念日有哪些(請用API Call)?")
QQ="2024年台灣10月紀念日有哪些?"
print(QQ)
RR = generate_hw02(QQ)
#"""

#RR = demo(QQ)
#print(RR.content)

