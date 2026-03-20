from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import wikipedia
from google import genai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
client = genai.Client(api_key="YOUR_API_KEY_HERE")
class NameRequest(BaseModel):
    name: str

class QueryRequest(BaseModel):
    query: str

# ---- MEMORY ----
memory = {
    "name": None,
    "last_topic": None
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

    # GREETING
    if "hello" in query:
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
    # WIKIPEDIA
    elif "who is" in query or "what is" in query:
        try:
            topic = query.replace("who is", "").replace("what is", "").strip()
            memory["last_topic"] = topic
            summary = wikipedia.summary(topic, sentences=2)
            return {"response": summary}
        except wikipedia.DisambiguationError as e:
            return {"response": "There are multiple matches. Please be more specific."}
        except wikipedia.PageError as e:
            return {"response": "I couldn't find any information on that topic."}

    elif"more" in query:
        return{"response":wiki_more()}
    elif"more"in query or"is that correct" in query:
        print("Accoding to google")
        return {"response": gemini_response.text}
    elif "your name" in query:
        return {"response": "Sorry I don't have a name yet."}
    elif "wrong" in query:
        print("Let me check again")
        print("Accoding to google")
        return {"response": gemini_response.text}
    # DEFAULT
    else:
        return {"response": "I don't understand yet."}