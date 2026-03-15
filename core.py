from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NameRequest(BaseModel):
    name: str

class QueryRequest(BaseModel):
    query: str

user_names = {}

@app.post("/set_name")
def set_name(req: NameRequest):
    return {"message": f"Hi {req.name}"}

@app.post("/query")
def process_query(req: QueryRequest):
    query = req.query.lower()
    if "hello" in query:
        return {"response": "Hi there!"}
    elif "bye" in query:
        return {"response": "Goodbye!"}
    else:
        return {"response": "I don't understand yet."}