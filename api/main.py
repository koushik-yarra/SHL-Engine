from fastapi import FastAPI
from pydantic import BaseModel
from backend.vector_search import search

app = FastAPI()
import os

@app.get("/")
def read_root():
    return {"status": "ok"}

class Query(BaseModel):
    query: str


@app.post("/recommend")
def recommend(q: Query):
    return search(q.query, top_k=5)


if __name__ == "__main__":
    # read PORT and convert to int (railway injects PORT as a string)
    port = int(os.getenv("PORT", 8000))
    # module path must match uvicorn command if someone runs `python api/main.py`
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, log_level="info")
