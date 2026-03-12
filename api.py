from fastapi import FastAPI
from pydantic import BaseModel

from main import generate_answer, search_similar_chunks

app = FastAPI(title="Second Brain API")


class ChatRequest(BaseModel):
    question: str


@app.get("/")
def read_root():
    return {"message": "Le serveur run"}


@app.post("/chat")
def chat_with_brain(request: ChatRequest):

    question = request.question

    results = search_similar_chunks(question)
    if len(results) == 0:
        return {"answer": "Aucun contexte trouvé dans la BD"}
    else:
        final_answer = generate_answer(question, results)

    return {"answer": final_answer}
