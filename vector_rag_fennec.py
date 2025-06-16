
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from llama_cpp import Llama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader

docs = TextLoader("Bizee_rules.txt").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(docs)
vectordb = Chroma.from_documents(chunks, embedding=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2"))

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

llm = Llama(
    model_path="./mistral-7b-instruct-v0.1.Q4_K_M.gguf",
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
