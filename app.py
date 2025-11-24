import streamlit as st
import requests

# 👉 Replace this with YOUR Railway backend URL
API_URL = "https://web-production-30ff8.up.railway.app/recommend"

st.set_page_config(page_title="SHL Recommendation Engine", page_icon="🔍")

st.title("🔍 SHL Assessment Recommendation Engine")

st.write(
    "Enter a job description or hiring query below to get SHL assessment recommendations."
)

query = st.text_area(
    "Job Description / Query",
    height=150,
    placeholder="Example: Hiring a Java developer with teamwork and problem-solving skills..."
)

if st.button("Recommend"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                response.raise_for_status()

                results = response.json()

                if len(results) == 0:
                    st.error("No recommendations found.")
                else:
                    st.subheader("Recommended Assessments")
                    for item in results:
                        st.markdown(f"### 📌 {item['name']}")
                        st.markdown(f"🔗 **URL:** [{item['url']}]({item['url']})")
                        st.write(item["description"])
                        st.markdown("---")

            except Exception as e:
                st.error(f"Error: {e}")

st.markdown("---")
st.caption("Built for SHL AI Research Intern Assignment — by Koushik 💼")
