
import google.generativeai as genai


model = genai.GenerativeModel('gemini-pro')

def optimisation_ai_help(code, question, language):
    response = model.generate_content("I am trying to solve the following problem:\n" + question + "\n\nMy code is:\n" + code + "\n\nI am using " + language + " to solve this problem.\n\n. Now help me in optimizing this code. Remember, don't give me the solution, just help me in optimizing my code. Do not give any code. Just answer in few lines.")
    return response.text