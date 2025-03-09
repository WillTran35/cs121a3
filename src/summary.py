from google import genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="environment.env")
key = os.getenv("API_KEY")

def getResponse(text):

    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=f"summarize this text {text} into 25 words or less please"
    )
    print(response.text)