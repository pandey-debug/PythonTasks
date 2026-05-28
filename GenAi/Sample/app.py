# To run this code you need to install the following dependencies:
# pip install google-genai

import os


from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()
def generate(question):
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-3-flash-preview"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=question),
            ],
        ),
    ]
    
    

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        
    ):
        if text := chunk.text:
            print(text, end="")

if __name__ == "__main__":
    question = input("Enter your question: ")
    generate(question)
