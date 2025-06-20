
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
import os
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

# determine rules path from environment
RULES_FILE = os.getenv("RULES_FILE", "Bizee_rules.txt")
docs = TextLoader(RULES_FILE).load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
vectordb = Chroma.from_documents(chunks, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

app = FastAPI()

# determine allowed CORS origins from environment, comma separated
default_origins = "http://localhost:3000"
origins_str = os.getenv("ALLOWED_ORIGINS", default_origins)
origins = [o.strip() for o in origins_str.split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = os.getenv("MODEL_PATH", "./mistral-7b-instruct-v0.1.Q4_K_M.gguf")
PORT = int(os.getenv("PORT", "8000"))

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048, n_threads=8, n_gpu_layers=35,
    chat_format="mistral-instruct"
)

SYSTEM_PROMPT = (
    "You are FENNEC, a legal assistant trained for business filings. "
    "Be concise and factual, quoting relevant Bizee rules."
)

@app.post("/api/chat")
async def chat(req: Request):
    q = (await req.json()).get("prompt", "").strip()
    if not q:
        return {"response": "Please ask about filing or compliance."}

    relevant = vectordb.similarity_search(q, k=3)
    context = "\n".join(chunk.page_content for chunk in relevant)

    resp = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": f"{SYSTEM_PROMPT}\n\nContext:\n{context}"},
            {"role": "user", "content": q}
        ],
        temperature=0.2, max_tokens=192
    )
    return {"response": resp["choices"][0]["message"]["content"].strip()}
