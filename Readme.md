
# SHL Assessment Recommendation Engine

AI-assisted tooling to scrape SHL’s public product catalog, clean the data, embed assessment descriptions with Gemini, index them in FAISS, and expose instant recommendations over a FastAPI + Streamlit UI. The search stack now also reranks the FAISS hits with Gemini 1.5 Flash for extra relevance.

---

## Key Features
- Automated catalog scraper with graceful pagination + detail-page enrichment.
- Cleaning + normalization pipeline that saves ready-to-embed JSONL files.
- Gemini `text-embedding-004` vectors stored in NumPy and queried via FAISS.
- Gemini 1.5 Flash reranker that reorders FAISS hits with lightweight LLM reasoning.
- FastAPI microservice (`/recommend`) for low-latency semantic search.
- Streamlit frontend with shareable Railway-friendly configuration.

---

## Repository Layout
```
.
├── api/                 # FastAPI service (uvicorn entry point at api/main.py)
├── app.py               # Streamlit client hitting the recommend endpoint
├── backend/             # Data prep, scraping, embedding, FAISS utilities
├── dataset/             # Provided Excel catalogue from SHL (input to scraper)
├── indexes/             # Generated artifacts (metadata.jsonl, embeddings, FAISS)
├── requirements.txt     # Shared Python deps for API + tooling
└── Procfile             # Railway process declaration
```

---

## Prerequisites
- Python 3.10+
- `pip` / `venv`
- Google Gemini API key (`GEMINI_API_KEY`) with access to `text-embedding-004`

---

## Setup
```bash
git clone <repo-url> shl-recommender
cd shl-recommender
python -m venv .venv && .venv\Scripts\activate      # or source .venv/bin/activate
pip install -r requirements.txt

# put secrets in .env (used by both backend scripts and FastAPI)
echo GEMINI_API_KEY=YOUR_KEY_HERE > .env
```

> Note: the `indexes/` folder already contains pre-built artifacts for quick starts. Rebuild only if you change the dataset or scraper.

---

## Data & Index Pipeline (optional rebuild)
1. **Scrape catalog**
   ```bash
   python backend/scraper.py
   ```
   Saves rich metadata into `indexes/metadata.jsonl`.

2. **Clean useful fields**
   ```bash
   python backend/ingest.py
   ```
   Produces `indexes/clean.jsonl`.

3. **Generate embeddings**
   ```bash
   python backend/embed.py
   ```
   Calls Gemini; stores `indexes/embeddings.npy`.

4. **Build FAISS index**
   ```bash
   python backend/build_faiss.py
   ```
   Writes `indexes/index.faiss` (flat L2).

---

## Run the Recommendation API
```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```
- Expects `GEMINI_API_KEY` in environment or `.env`.
- `backend/vector_search.py` automatically loads the FAISS artifacts and reranks the top FAISS hits with Gemini 1.5 Flash (JSON index ordering). Set `GEMINI_API_KEY` with access to both the embedding and flash models.
- Health check: `GET /` → `{"status": "ok"}`.
- Recommend:
  ```bash
  curl -X POST http://localhost:8000/recommend \
       -H "Content-Type: application/json" \
       -d '{"query": "hiring a Java developer with teamwork skills"}'
  ```
  Response is a list of `{name, url, description}` objects.

---

## Run the Streamlit UI
1. Edit `API_URL` in `app.py` (line 5) to point at your FastAPI deployment.
2. Launch:
   ```bash
   streamlit run app.py
   ```
3. Enter a job description to see top SHL assessments with links.

---

## Deployment Notes
- **Railway / Render**: use `Procfile` (`web: uvicorn api.main:app --host 0.0.0.0 --port $PORT`).
- **Environment variables**: `GEMINI_API_KEY` (required), `PORT` (platform-provided).
- **Frontend**: redeploy Streamlit separately or host via Streamlit Community Cloud; update `API_URL`.

---

## Troubleshooting
- *Gemini errors*: ensure quota + correct API key; retries are not built-in.
- *Empty results*: verify FAISS artifacts exist and match `clean.jsonl` length.
- *Large scrapes*: scraper already delays between requests; further tune `time.sleep` if blocked.

---

## Future Enhancements
- Toggle reranking on/off per request.
- Cache embeddings for repeated queries.
- Add automated tests and CI for scraper failures.

---

Built for SHL AI Research Intern assignment – feel free to fork and extend.

