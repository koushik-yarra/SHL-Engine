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


'''def search(query: str, top_k: int = 5):
    q_emb = embed_query(query)
    q_emb = np.expand_dims(q_emb, axis=0)

    distances, idx = index.search(q_emb, top_k)

    results = []
    for i in idx[0]:
        if i < len(records):
            results.append(records[i])

    return results
'''
#  use this code if you want to rerank with LLM  for better answers
def rerank_with_llm(query, results):
    prompt = f"""
    You are an SHL assessment expert. 
    Given this job description/query:
    {query}

    And these assessments:
    {results}

    Re-rank them from most relevant to least relevant.
    Return only a JSON list of indices sorted by relevance.
    """

    llm_resp = genai.generate_text(
        model="gemini-1.5-flash",
        prompt=prompt
    )

    import json
    try:
        sorted_idx = json.loads(llm_resp.text.strip())
        return [results[i] for i in sorted_idx]
    except:
        return results


# and improve search with this
def search(query: str, top_k: int = 5):
    q_emb = embed_query(query)
    q_emb = np.expand_dims(q_emb, axis=0)

    distances, idx = index.search(q_emb, top_k)

    results = [records[i] for i in idx[0] if i < len(records)]

    # 🔥 Add LLM-based reranking here
    results = rerank_with_llm(query, results)

    return results
