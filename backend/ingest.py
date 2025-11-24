from backend.utils import METADATA_JSONL, CLEAN_JSONL, read_jsonl, write_jsonl

def clean_record(r):
    return {
        "name": r.get("name", "").strip(),
        "url": r.get("url", "").strip(),
        "description": r.get("description", "").strip(),
    }

def main():
    records = read_jsonl(METADATA_JSONL)
    cleaned = [clean_record(r) for r in records if r.get("name")]
    write_jsonl(CLEAN_JSONL, cleaned)
    print(f"Cleaned {len(cleaned)} records → {CLEAN_JSONL}")

if __name__ == "__main__":
    main()
