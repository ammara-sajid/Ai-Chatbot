from gpt4all import GPT4All
from sentence_transformers import SentenceTransformer
from pinecone import Pinecone
from config import PINECONE_API_KEY

# Load GPT4All model
MODEL_NAME = "Llama-3.2-1B-Instruct-Q4_0.gguf"   # or whichever you downloaded
llm = GPT4All(model_name=MODEL_NAME)

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Connect Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index("company-knowledge")

def retrieve_context(query, top_k=3):
    vector = embedder.encode(query).tolist()
    results = index.query(vector=vector, top_k=top_k, include_metadata=True)
    context = "\n".join([m["metadata"]["text"] for m in results["matches"]])
    return context

def ask_llm(question):
    # 1. Retrieve relevant context
    context = retrieve_context(question)

    # 2. Build a prompt for GPT4All
    prompt = f"""
    You are an assistant with access to PARCO company knowledge.
    Use the following context to answer the question.

    Context:
    {context}

    Question: {question}
    Answer:
    """

    # 3. Generate an answer
    with llm.chat_session() as session:   # ✅ keeps context across turns
    response = llm.generate(prompt, max_tokens=300)
return response

if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or 'exit'): ")
        if q.lower() == "exit":
            break
        answer = ask_llm(q)
        print("\n🤖", answer)
