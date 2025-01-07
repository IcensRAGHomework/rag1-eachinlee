import json
import traceback
import re

from rich import print as pprint
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from model_configurations import get_model_configuration
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage

gpt_chat_version = 'gpt-4o'
gpt_config = get_model_configuration(gpt_chat_version)

def generate_hw01(question):
    question = question + "以JSON格式輸出外層為Result:，每筆資料包含date:只需要顯示日期與name:顯示紀念日名稱，以西元年開頭YYYY-MM-DD 格式顯示日期，再換行顯示紀念日名稱，最後不需顯示任何其他注意資訊，"
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

    #print response as JSON object
    #print(response.content)

    #try to apply JsonOutputParser()

    json_parser = JsonOutputParser()
    json_output = json_parser.invoke(response)
    print(json_output)

    return response
    


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






#Test generate_hw01
print("generate_hw01 請回答台灣特定月份的紀念日有哪些(請用JSON格式呈現)?")
QQ="2025年台灣6月紀念日有哪些?"
print(QQ)
RR = generate_hw01(QQ)

#RR = demo(QQ)
#print(RR.content)

