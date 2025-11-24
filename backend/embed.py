import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import os
from backend.utils import CLEAN_JSONL, EMBEDDINGS_NPY, read_jsonl

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBED_MODEL = "models/text-embedding-004"

def embed_texts(texts):
    vectors = []
    for t in texts:
        resp = genai.embed_content(
            model=EMBED_MODEL,
            content=t
        )
        vectors.append(resp["embedding"])
    return np.array(vectors, dtype="float32")


def main():
    records = read_jsonl(CLEAN_JSONL)
    texts = [r["name"] + " " + r["description"] for r in records]

    print(f"Embedding {len(texts)} items...")
    vectors = embed_texts(texts)

    np.save(EMBEDDINGS_NPY, vectors)
    print("Saved embeddings →", EMBEDDINGS_NPY)


if __name__ == "__main__":
    main()
