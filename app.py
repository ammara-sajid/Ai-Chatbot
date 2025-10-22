import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from gpt4all import GPT4All
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
MODEL_PATH = os.getenv("MODEL_PATH")

# Flask app
app = Flask(__name__)
CORS(app)

# Initialize Pinecone client
pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(PINECONE_INDEX)

# Embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load GPT4All model
llm = GPT4All(MODEL_PATH)

# ✅ Quick responses for common questions
QUICK_RESPONSES = {
    "hi": "Hi! How can I assist you about PARCO today?",
    "hello": "Hi! How can I assist you about PARCO today?",
    "hey": "Hi! How can I assist you about PARCO today?",
    "what is parco?": "PARCO (Pak-Arab Refinery Limited) is a Pakistani oil refining company. It operates refineries, pipelines, and fuel distribution.",
    "who owns parco?": "PARCO is a joint venture between the Government of Pakistan and the Emirate of Abu Dhabi.",
    "where is parco located?": "PARCO’s main refinery is located in Mahmoodkot, Multan, Pakistan."
}

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # ✅ Quick lookup first (case insensitive)
    if user_message.lower() in QUICK_RESPONSES:
        return jsonify({"reply": QUICK_RESPONSES[user_message.lower()]})

    # Step 1: Create embedding for user query
    query_embedding = embedder.encode(user_message).tolist()

    # Step 2: Search Pinecone index for relevant context
    results = index.query(vector=query_embedding, top_k=3, include_metadata=True)

    # Step 3: Collect retrieved text chunks
    context = " ".join([match["metadata"].get("text", "") for match in results.get("matches", [])])

    if not context.strip():
        context = "Sorry, I could not find relevant information in PARCO knowledge base."

    # Step 4: Generate reply with strict rules
    prompt = f"""
You are a helpful AI assistant that only answers about PARCO (Pak-Arab Refinery Limited).

Rules:
- Only answer the user’s question directly.
- Do not invent questions or simulate extra conversation.
- If the context does not contain the answer, reply politely with "Sorry, I don’t know about that."

Context: {context}

User: {user_message}
Answer:
"""

    with llm.chat_session():
        reply = llm.generate(prompt, max_tokens=200)

    # ✅ Post-process reply: remove any extra role-play
    if "User:" in reply:
        reply = reply.split("User:")[0].strip()
    if "AI:" in reply:
        reply = reply.split("AI:")[0].strip()

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
