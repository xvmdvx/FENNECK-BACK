## fennec_server_chatfmt_fixed.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
import logging

MODEL_PATH = "./mistral-7b-instruct-v0.1.Q4_K_M.gguf"

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# Chat format corregido
logger = logging.getLogger(__name__)
llm = None
try:
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=8,
        n_gpu_layers=35,
        chat_format="mistral-instruct"
    )
except Exception as e:
    logger.exception(f"Failed to load model at {MODEL_PATH}: {e}")

SYSTEM_PROMPT = (
    "You are FENNEC, an expert virtual assistant trained to help US business filing agents.\n"
    "You only answer questions about entity formation, BOIR, compliance, and state filing rules.\n"
    "Keep your responses concise (1–3 sentences), professional, and factual.\n"
)

@app.post("/api/chat")
async def chat(req: Request):
    data = await req.json()
    user_msg = data.get("prompt", "").strip()
    if not user_msg:
        return {"response": "How can I assist you with your business filing or compliance question?"}
    if llm is None:
        return {"error": "Language model is not available"}
    resp = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_msg}
        ],
        temperature=0.2,
        max_tokens=192
    )
    answer = resp["choices"][0]["message"]["content"].strip()
    return {"response": answer}
