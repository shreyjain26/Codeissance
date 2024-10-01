import os
import requests
from dotenv import load_dotenv
# import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


# genai.configure(api_key=GEMINI_API_KEY)
     
# model = genai.GenerativeModel('gemini-1.5-flash')


def call_gemini_api(prompt, max_tokens=500, temperature=0.5):
    response = model.generate_content(
        contents=prompt,
        # stream=True,
        generation_config=genai.types.GenerationConfig(
        max_output_tokens=max_tokens,
        temperature=temperature,
        )
    )
    return response.text
