from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer

# Initialize FastAPI
app = FastAPI()

# Load the SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Ensure path exists
collection = chroma_client.get_or_create_collection("subtitles")

# Define request model
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5  # Default: top 5 results

# API Endpoint to Search Subtitles
@app.post("/search/")
async def search_subtitles(request: SearchRequest):
    query_embedding = model.encode(request.query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding], n_results=request.top_k
    )

    response = []
    for i in range(len(results["ids"][0])):
        response.append({
            "subtitle": results["documents"][0][i],
            "score": results["distances"][0][i]
        })

    return {"query": request.query, "results": response}

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "FastAPI server for Subtitle Search is running!"}
