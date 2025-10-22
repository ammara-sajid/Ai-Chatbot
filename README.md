# 🤖 AI Chatbot Android Application – PARCO Project

This project is an **AI-powered chatbot Android application** developed for **PARCO (Pak-Arab Refinery Company)**.  
The chatbot integrates a **Flask backend**, **GPT4All** (local AI model), and **Pinecone vector database** to provide **contextual and intelligent conversational responses** through a **Flutter-based mobile interface**.

---

## 🧠 Features
- 💬 Real-time AI chatbot with contextual understanding  
- 🔗 Flask backend integrated with GPT4All and Pinecone  
- 📱 Flutter-based Android user interface  
- 🌐 Secure communication using REST APIs via **ngrok tunneling**  
- 🧩 Embedding and semantic search using **Sentence Transformers**

---

## 🏗️ Tech Stack

| Layer | Technology |
|--------|-------------|
| **Frontend (Mobile)** | Flutter, Dart |
| **Backend** | Python (Flask) |
| **AI Model** | GPT4All |
| **Vector Database** | Pinecone |
| **Embeddings** | Sentence Transformers |
| **Networking** | Ngrok for tunneling |
| **Environment** | Localhost / Flask Server |

---

## ⚙️ Project Workflow

1. **User Input** – User enters a message in the Flutter app.  
2. **API Request** – The message is sent to the Flask backend through REST API.  
3. **Embedding Generation** – Sentence Transformers convert the input into embeddings.  
4. **Context Retrieval** – Pinecone retrieves relevant context.  
5. **Response Generation** – GPT4All generates a human-like response.  
6. **Display** – The response is sent back and displayed in the Flutter UI.

---

## 📸 App Preview

(Add screenshots or GIFs of your app interface — e.g., chat screen, backend running, etc.)

---

## 🚀 How to Run

### Backend (Flask)
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chatbot-parco.git

## 🖥️ Frontend (Flutter)

1. Open the Flutter project in **Android Studio** or **VS Code**.  
2. Update the base URL in `ApiService.dart` with your **ngrok link**.  
3. Run the app on an emulator or Android device:
   ```bash
   flutter run

## 📚 Learning Outcomes

- Gained hands-on experience in **AI integration** with mobile applications.  
- Understood **Flask API communication** with a **Flutter frontend**.  
- Explored **semantic search** using **embeddings and vector databases**.  

---

## 💡 Future Enhancements

- Add **voice input and output** support.  
- Improve **chat history and memory management**.  
- Deploy the backend to a **cloud server** for persistent hosting.  

---

## 👩‍💻 Author

**Ammara Sajid**  
Developed as part of an **AI project for PARCO (Pak-Arab Refinery Company)**  
