from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
INDEX_DIR = ROOT / "indexes"

METADATA_JSONL = INDEX_DIR / "metadata.jsonl"
CLEAN_JSONL = INDEX_DIR / "clean.jsonl"
EMBEDDINGS_NPY = INDEX_DIR / "embeddings.npy"
FAISS_INDEX = INDEX_DIR / "index.faiss"


def read_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                items.append(json.loads(line))
    return items


def write_jsonl(path, records):
    with open(path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
