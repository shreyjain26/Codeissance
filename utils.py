import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import base64
from io import BytesIO

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')


genai.configure(api_key=GEMINI_API_KEY)
     
model = genai.GenerativeModel('gemini-1.5-flash')


def call_gemini_api(prompt,img,  max_tokens=500, temperature=0.5):
    # print(img)
    # img = base64.b64encode(img).decode('utf-8')
    img = Image.open(img)
    response = model.generate_content(
        contents=[img, prompt],
        # stream=True,
        # image_input= img,
        generation_config=genai.types.GenerationConfig(
        max_output_tokens=max_tokens,
        temperature=temperature,
        )
    )
    return response.text
