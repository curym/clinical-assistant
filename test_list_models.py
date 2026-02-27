from dotenv import load_dotenv
import os
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("\nModelos disponíveis no projeto:\n")

for model in client.models.list():
    print(f"- {model.name}")
    if hasattr(model, "description"):
        print(f"  descrição: {model.description}")
    print()
