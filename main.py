from gpt4all import GPT4All

# Pick the model you want (name must match from list_models)
model = GPT4All("Meta-Llama-3-8B-Instruct.Q4_0.gguf")

# Start a chat session
with model.chat_session() as session:
    response = model.generate("Hello! How are you?")
    print(response)
