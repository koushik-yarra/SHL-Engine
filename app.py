import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/recommend"

st.title("🔍 SHL GenAI Assessment Recommendation Engine")
query = st.text_area("Enter your query:", height=120)

if st.button("Recommend"):
    if query.strip():
        res = requests.post(API_URL, json={"query": query})
        data = res.json()

        for item in data:
            st.subheader(item["name"])
            st.write(item["url"])
            st.write(item["description"])
            st.markdown("---")
