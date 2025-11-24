import { useState } from "react";

export default function Home() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  // 👉 Replace with YOUR backend URL
  const API_URL = "https://web-production-30ff8.up.railway.app/recommend";

  async function handleSearch() {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await response.json();
      setResults(data);
    } catch (err) {
      console.error(err);
      alert("Error fetching recommendations.");
    }

    setLoading(false);
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "Arial" }}>
      <h1 style={{ fontSize: "30px", marginBottom: "20px" }}>
        🔍 SHL Assessment Recommendation Engine
      </h1>

      <textarea
        placeholder="Enter your query or job description..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={6}
        style={{
          width: "100%",
          padding: "12px",
          fontSize: "16px",
          borderRadius: "8px",
          border: "1px solid #ccc",
        }}
      />

      <button
        onClick={handleSearch}
        style={{
          padding: "10px 20px",
          fontSize: "18px",
          marginTop: "15px",
          cursor: "pointer",
          background: "#0070f3",
          color: "white",
          border: "none",
          borderRadius: "8px",
        }}
      >
        Recommend
      </button>

      {loading && <p style={{ marginTop: "20px" }}>Loading...</p>}

      {results.length > 0 && (
        <div style={{ marginTop: "30px" }}>
          {results.map((item, i) => (
            <div
              key={i}
              style={{
                padding: "15px",
                border: "1px solid #eee",
                borderRadius: "10px",
                marginBottom: "20px",
                background: "#fafafa",
              }}
            >
              <h2>{item.name}</h2>
              <a href={item.url} target="_blank" rel="noreferrer">
                {item.url}
              </a>
              <p style={{ marginTop: "10px" }}>{item.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
