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
    #"""
    #Setup Prompt  
    prompt_tmp = PromptTemplate.from_template("以下列格式輸出{format_set}，且注意此條件{condition_set}")
    prompt_str = prompt_tmp.format(
    format_set="請生成一個 JSON 物件，包含一個名為 Result的屬性，該屬性下有兩個子屬性： date :YYYY-MM-DD  和 name :紀念日名稱",
    condition_set="最後不需顯示任何其他資訊")

    question = question + prompt_str
    #"""

    #Use Demo function to process LLM API
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





#"""
#Test generate_hw01
print("generate_hw01 請回答台灣特定月份的紀念日有哪些(請用JSON格式呈現)?")
QQ="2023年台灣4月紀念日有哪些?"
print(QQ)
RR = generate_hw01(QQ)
#"""




#RR = demo(QQ)
#print(RR.content)

