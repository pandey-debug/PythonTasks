import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(request: PromptRequest):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    def stream():
        response = client.models.generate_content_stream(
            model="gemini-3-flash-preview",
            contents=request.prompt
        )
        for chunk in response:
            if chunk.text:
                yield chunk.text

    return StreamingResponse(stream(), media_type="text/plain")