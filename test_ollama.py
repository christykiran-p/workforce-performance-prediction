import time
import ollama

client = ollama.Client(host="http://localhost:11434")

print("Connecting...")

start = time.time()

response = client.chat(
    model="phi3:latest",
    messages=[
        {
            "role": "user",
            "content": "Say Hello in one sentence."
        }
    ]
)

print("Time:", round(time.time() - start, 2), "seconds")
print(response["message"]["content"])