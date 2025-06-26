import os
from dotenv import load_dotenv
import ollama
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from email_reply_parser import EmailReplyParser

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
ollama.base_url = OLLAMA_HOST

app = FastAPI(title="Email Extractor API")

PROMPT_TEMPLATE = (
    "From the text below, return exactly the email content beginning including the first greeting "
    "(e.g., 'Hi', 'Hello') and ending with the sender's final sign‑off line including that line that contains the name of the preson if present in signoff. "
    "Preserve original line breaks and spacing. Do NOT add any extra words, labels, or quotation marks.\n---\n{latest}\n---"
)

def extract(txt: str, model: str) -> str:
    latest = EmailReplyParser.read(txt).reply.strip()
    prompt = PROMPT_TEMPLATE.format(latest=latest)
    res = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return res["message"]["content"].strip()

@app.post("/extract", response_class=JSONResponse)
async def api(request: Request):
    try:
        email_text = (await request.body()).decode("utf-8")
        cleaned = extract(email_text, OLLAMA_MODEL)
        return {"content": cleaned}
    except Exception as e:
        raise HTTPException(500, f"Ollama error: {e}")