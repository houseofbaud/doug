import requests
from os import environ
from dotenv import load_dotenv

load_dotenv()

if environ.get("OPENAI_API_KEY") is None:
    print("ERROR: OpenAI API Key is not set")
    exit(1)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {environ.get('OPENAI_API_KEY')}"
}

url = "https://api.openai.com/v1/models"

response = requests.get(url, headers=headers)

if response.status_code == 200:
    models = response.json()["data"]
    for model in models:
        print(model["id"])
else:
    print("Error: Unable to retrieve list of models.")
