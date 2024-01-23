
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
    ai_backend = "gemini"
    if ai_backend=="gemini":
        response = model.generate_content(prompt)
        return response.text
    else:
        completion = client.chat.completions.create(model="gpt35",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ])
        return completion.choices[0].message.content


def ai_chat(chat_history, query):
    chat_history.append({"role": "user", "parts": [query]})
    response = model.generate_content(chat_history)
    chat_history.append({"role": "model", "parts": [response.text]})
    return chat_history, response.text

