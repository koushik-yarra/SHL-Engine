import numpy as np
import faiss
import google.generativeai as genai
from backend.utils import CLEAN_JSONL, read_jsonl, FAISS_INDEX
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "models/text-embedding-004"

records = read_jsonl(CLEAN_JSONL)
index = faiss.read_index(str(FAISS_INDEX))


def embed_query(q: str):
    resp = genai.embed_content(
        model=EMBED_MODEL,
        content=q
    )
    return np.array(resp["embedding"], dtype="float32")


def search(query: str, top_k: int = 5):
    q_emb = embed_query(query)
    q_emb = np.expand_dims(q_emb, axis=0)

    distances, idx = index.search(q_emb, top_k)

    results = []
    for i in idx[0]:
        if i < len(records):
            results.append(records[i])

    return results
