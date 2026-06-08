from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import wikipedia
import warnings
import requests
from dotenv import load_dotenv

warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

# -------- REQUEST MODELS --------

class NameRequest(BaseModel):
    name: str


class QueryRequest(BaseModel):
    query: str


# -------- MEMORY --------

memory = {
    "name": None,
    "last_topic": None,
    "last_query": None
}


# -------- SET NAME --------

@app.post("/set_name")
def set_name(req: NameRequest):
    memory["name"] = req.name
    return {"message": f"Hi {req.name}"}


# -------- MAIN QUERY --------

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


    # ABOUT BOT

    elif "who are you" in query:

        return {
            "response": "I am Chatbot version 2.2, a personal AI assistant."
        }


    # STORE NAME

    elif "my name is" in query:

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


    # BOT NAME

    elif "your name" in query:

        return {"response": "My name is Chatbot version 2.2."}


    # WIKIPEDIA SEARCH

    elif any(x in query for x in ["who is", "what is", "where is"]):

        try:

            topic = (
                query.replace("who is", "")
                .replace("where is", "")
                .replace("what is", "")
                .strip()
            )

            memory["last_topic"] = topic

            summary = wikipedia.summary(topic, sentences=2)

            return {
                "response": f"{summary}\n\nDid you want me to check with AI?"
            }

        except wikipedia.DisambiguationError:

            return {
                "response": "There are multiple matches. Please be more specific."
            }

        except wikipedia.PageError:

            return {
                "response": "I couldn't find any information on that topic."
            }


    # REFER AI (OLLAMA VIA HTTP)

    elif any(k in query for k in ["more", "yes", "refer ollama", "refer ai"]):

        ollama_query = query

        if memory.get("last_query"):
            ollama_query = f"more on it {memory['last_query']}"

        try:

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3.2",
                    "messages": [
                        {"role": "user", "content": ollama_query}
                    ]
                }
            )

            return {
                "response": response.json()["message"]["content"]
            }

        except Exception as e:

            return {
                "response": f"Ollama connection error: {str(e)}"
            }


    # WRONG RESPONSE CORRECTION

    elif "wrong" in query:

        try:

            wrong_query = f"I was wrong about: {memory.get('last_query', '')}. Can you correct me?"

            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "llama3.2",
                    "messages": [
                        {"role": "user", "content": wrong_query}
                    ]
                }
            )

            return {
                "response": response.json()["message"]["content"]
            }

        except Exception as e:

            return {
                "response": f"Ollama connection error: {str(e)}"
            }


    # DEFAULT RESPONSE

    else:

        return {"response": "I don't understand yet."}