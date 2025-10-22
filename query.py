from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from config import PINECONE_API_KEY

# Load same model you used for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("company-knowledge")

def query_pinecone(question, top_k=3):
    # Convert question to vector
    vector = model.encode(question).tolist()

    # Search in Pinecone
    result = index.query(vector=vector, top_k=top_k, include_metadata=True)

    print("\n🔍 Search Results:")
    for match in result["matches"]:
        print(f"- Score: {match['score']:.3f}")
        print(f"  Text: {match['metadata']['text']}")
        print(f"  Source: {match['metadata']['url']}\n")

if __name__ == "__main__":
    user_q = input("Ask a question: ")
    query_pinecone(user_q)
