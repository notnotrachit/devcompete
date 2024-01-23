
import google.generativeai as genai
from openai import AzureOpenAI
import os
from openai import AzureOpenAI

client = AzureOpenAI(azure_endpoint="https://devcompete-ai.openai.azure.com/",
api_version="2023-07-01-preview",
api_key=os.getenv("OPENAI_API_KEY"))
from openai import OpenAI


deployment_name='gpt35'

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

model = genai.GenerativeModel('gemini-pro')

def optimisation_ai_help(code, question, language):
    prompt="I am trying to solve the following problem:\n" + question + "\n\nMy code is:\n" + code + "\n\nI am using " + language + " to solve this problem.\n\n. Now help me in optimizing this code. Remember, don't give me the solution, just help me in optimizing my code. Do not give any code. Just answer in few lines."
    # response = model.generate_content(prompt)
    # response = client.completions.create(model=deployment_name, prompt=prompt)
    completion = client.chat.completions.create(model="gpt35",
    # messages=prompt)
      messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": prompt}
  ])
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
    # return response.text


def ai_chat(chat_history, query):
    response = model.generate_content(chat_history + "\n\n" + query)
    return response.text
