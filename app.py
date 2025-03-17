import streamlit as st
import requests

# Backend API URL (Ensure FastAPI is running)
API_URL = "http://127.0.0.1:8000/search/"

# Streamlit UI
st.title("🎬 Subtitle Search Engine")
st.write("Search for subtitles using keyword-based or semantic search.")

# User input
query = st.text_input("Enter your search query:")
top_k = st.slider("Number of results:", min_value=1, max_value=10, value=5)

if st.button("Search"):
    if query.strip():
        st.info(f"Searching for: {query}")

        # Make API request to FastAPI backend
        response = requests.post(API_URL, json={"query": query, "top_k": top_k})

        if response.status_code == 200:
            results = response.json().get("results", [])
            
            if results:
                st.subheader("🔍 Search Results:")
                for result in results:
                    st.write(f"- **{result['subtitle']}** (Score: {result['score']:.4f})")
            else:
                st.warning("No matching subtitles found.")
        else:
            st.error("Error fetching results. Please check if the backend is running.")
    else:
        st.warning("Please enter a valid search query.")
