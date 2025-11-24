import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const API_URL = "https://shl-engine.onrender.com/recommend"; // your backend

  async function handleSearch() {
    if (!query.trim()) return;

    setLoading(true);
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();
    setResults(data);
    setLoading(false);
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "Arial" }}>
      <h1>🔍 SHL Assessment Recommendation Engine</h1>

      <textarea
        placeholder="Enter your query..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={7}
        style={{ width: "100%", padding: 10, fontSize: 16 }}
      />

      <button
        onClick={handleSearch}
        style={{
          padding: "10px 20px",
          fontSize: 18,
          marginTop: 15,
          cursor: "pointer",
        }}
      >
        Recommend
      </button>

      {loading && <p>Loading...</p>}

      {results.length > 0 && (
        <div style={{ marginTop: 30 }}>
          {results.map((item, i) => (
            <div
              key={i}
              style={{
                padding: 15,
                border: "1px solid #ddd",
                borderRadius: 8,
                marginBottom: 20,
              }}
            >
              <h2>{item.name}</h2>
              <a href={item.url} target="_blank" rel="noreferrer">
                {item.url}
              </a>
              <p style={{ marginTop: 10 }}>{item.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
