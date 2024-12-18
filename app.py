from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
import pinecone
import os

# Initialize FastAPI app
app = FastAPI()

from pinecone import Pinecone
import os

# Load Pinecone API key
pinecone_api_key = os.getenv("PINECONE_API_KEY")
if not pinecone_api_key:
    raise ValueError("PINECONE_API_KEY not found. Check your .env file or environment variables.")

# Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# Connect to the index
index = pc.Index("langchainvectors")

# Load the SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Pydantic model for input validation
class Query(BaseModel):
    query: str

# Endpoint to handle chatbot queries
@app.post("/ask")
async def ask_question(input_query: Query):
    # Generate embedding for the query
    query_embedding = model.encode(input_query.query).tolist()

    # Query Pinecone for the most relevant answer
    results = index.query(vector=query_embedding, top_k=1, include_metadata=True)

    if results["matches"]:
        answer = results["matches"][0]["metadata"]["text"]
    else:
        answer = "Sorry, I couldn't find an answer."

    return {"query": input_query.query, "answer": answer}

# Root endpoint for testing
@app.get("/")
async def root():
    return {"message": "Chatbot API is running!"}
