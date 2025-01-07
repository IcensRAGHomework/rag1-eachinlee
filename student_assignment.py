import json
import traceback
import re

from model_configurations import get_model_configuration
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):

    question = question + "請生成一個 JSON 物件，不需要顯示json字串，直接包含一個名為 Result的屬性，該屬性下有兩個子屬性： date :YYYY-MM-DD  和 name :紀念日名稱，只顯示國慶日，，不需顯示任何其他資訊，"
    #print(question)

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
    
    #json_parser = JsonOutputParser()
    #json_output = json_parser.invoke(response)
    #print(json_output)

    json_string = response.content

    print(json_string)

    parsed_data = json.loads(json_string)

    return json_string
    


def generate_hw02(question):
    pass
    
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

#RR = demo(QQ)
#print(RR.content)

