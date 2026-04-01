from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import wikipedia
import os
import warnings
from dotenv import load_dotenv
import ollama

warnings.filterwarnings("ignore", category=UserWarning, module='wikipedia')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
# Ollama runs locally, so no API key is typically needed.
# Ensure ollama is running: `ollama run llama3`

class NameRequest(BaseModel):
    name: str

class QueryRequest(BaseModel):
    query: str

# ---- MEMORY ----
memory = {
    "name": None,
    "last_topic": None,
    "last_query": None
}

# ---- SET NAME ----
@app.post("/set_name")
def set_name(req: NameRequest):
    memory["name"] = req.name
    return {"message": f"Hi {req.name}"}

# ---- MAIN QUERY ----
@app.post("/query")
def process_query(req: QueryRequest):
    query = req.query.lower()

    if not any(k in query for k in ["yes", "more", "is that correct", "wrong", "refer ollama", "refer ai"]):
        memory["last_query"] = req.query

    # GREETING
    if "hello" in query or "hi" in query or "hey" in query:
        if memory["name"]:
            return {"response": f"Hi {memory['name']}!"}
        return {"response": "Hi there!"}

    # TIME
    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return {"response": f"Current time is {current_time}"}

    # STORE NAME FROM CHAT
    elif "my name " in query:
        name = query.replace("my name is", "").strip()
        memory["name"] = name
        return {"response": f"Nice to meet you {name}!"}

    # RECALL NAME
    elif "know my name" in query:
        if memory["name"]:
            return {"response": f"Your name is {memory['name']}"}
        return {"response": "I don't know your name yet."}

    # EXIT
    elif "bye" in query:
        return {"response": "Goodbye!"}
        
    # YOUR NAME
    elif "your name" in query:
        return {"response": "Sorry I don't have a name yet."}
        
    # WIKIPEDIA
    elif any(x in query for x in ["who is", "what is", "where is"]):
        try:
            topic = query.replace("who is", "").replace("where is", "").replace("what is", "").strip()
            memory["last_topic"] = topic
            summary = wikipedia.summary(topic, sentences=2)
            return {"response": f"{summary}\n\ndid you need to refer ollama ?"}
        except wikipedia.DisambiguationError:
            return {"response": "There are multiple matches. Please be more specific."}
        except wikipedia.PageError:
            return {"response": "I couldn't find any information on that topic."}
    elif any(k in query for k in ["more", "is that correct", "yes", "refer ollama", "refer ai"]):
        print("According to ollama")
        ollama_query = query
        if any(k in query for k in ["yes", "more", "refer ollama", "refer ai"]):
            if memory.get("last_query"):
                ollama_query = f"more on it {memory['last_query']}"
        try:
            ollama_response = ollama.chat(
                model='llama3.2',
                messages=[{"role": "user", "content": ollama_query}],
            )
            return {"response": ollama_response['message']['content']}
        except Exception as e:
            return {"response": f"Ollama error: {str(e)}"}
        
    elif "your name" in query:
        return {"response": "Sorry I don't have a name yet."}
        
    elif "wrong" in query:
        print("Let me check again")
        print("According to ollama")
        try:
            wrong_query = f"I was wrong about: {memory.get('last_query', '')}. Can you correct me?"
            ollama_response = ollama.chat(
                model='llama3.2',
                messages=[{"role": "user", "content": wrong_query}],
            )
            return {"response": ollama_response['message']['content']}
        except Exception as e:
            return {"response": f"Ollama error: {str(e)}"}
        
    # DEFAULT
    else:
        return {"response": "I don't understand yet."}
