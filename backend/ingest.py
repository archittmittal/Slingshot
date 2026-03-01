import sys
import os
import requests
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

# Load config or set manually
QDRANT_URL = "https://your-qdrant-cluster-url"
QDRANT_API_KEY = "your-api-key"
COLLECTION_NAME = "campus_knowledge"

def ingest_text(text: str, metadata: dict = None):
    print(f"Initializing SentenceTransformer...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    print(f"Connecting to Qdrant...")
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
    
    # Create collection if not exists
    collections = client.get_collections().collections
    if not any(c.name == COLLECTION_NAME for c in collections):
        print(f"Creating collection {COLLECTION_NAME}...")
        from qdrant_client.http import models
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )

    print(f"Encoding text...")
    vector = model.encode(text).tolist()
    
    print(f"Uploading to Qdrant...")
    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": os.urandom(16).hex(),
                "vector": vector,
                "payload": {"text": text, **(metadata or {})}
            }
        ]
    )
    print("✅ Ingestion successful!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python ingest.py 'Your text here'")
    else:
        ingest_text(sys.argv[1])
