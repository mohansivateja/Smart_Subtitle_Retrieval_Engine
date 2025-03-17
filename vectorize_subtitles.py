import chromadb
from sentence_transformers import SentenceTransformer

# Load SentenceTransformer model
model = SentenceTransformer("all-MiniLM-L6-v2")
print("✅ SentenceTransformer model loaded successfully.")

# Connect to ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
print("✅ Connected to ChromaDB.")

# **Step 1: Delete Existing Subtitle Collection**
try:
    chroma_client.delete_collection("subtitles")
    print("✅ Old subtitle collection deleted.")
except Exception as e:
    print("⚠️ No existing collection found or error deleting:", e)

# **Step 2: Create New Subtitle Collection**
collection = chroma_client.get_or_create_collection("subtitles")

# **Step 3: Define Your Subtitle Data**
subtitles = [
    "Hyderabad is known as the City of Pearls.",
    "The Charminar is a famous monument in Hyderabad.",
    "Biryani from Hyderabad is world-famous.",
    "HITEC City is the tech hub of Hyderabad.",
    "The history of AI dates back to the 1950s.",
    "Deep learning is a subset of machine learning.",
    "Artificial intelligence is transforming industries.",
    "The Turing Test was proposed by Alan Turing to measure AI intelligence.",
    "Machine learning is fascinating!"
]

# **Step 4: Generate Embeddings for Subtitles**
subtitle_embeddings = model.encode(subtitles).tolist()

# **Step 5: Store Subtitles in ChromaDB**
for i, subtitle in enumerate(subtitles):
    collection.add(
        ids=[str(i)], 
        documents=[subtitle],  
        embeddings=[subtitle_embeddings[i]]  
    )

print("✅ New subtitles stored successfully!")

# **Step 6: Verify Storage**
stored_data = collection.get()
print(f"✅ Total Subtitles Stored: {len(stored_data['ids'])}")
