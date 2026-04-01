import ollama

try:
    response = ollama.chat(
        model='llama3.2',
        messages=[{"role": "user", "content": "hello"}]
    )
    print("Success:", response['message']['content'])
except Exception as e:
    print("Failed:", repr(e))
