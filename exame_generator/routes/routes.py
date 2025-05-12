from fastapi import FastAPI
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent / "models"))
from module.schemas import NotesInfoList, PaperFormat, PaperResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/notesinfo")
def read_notes_info():
    return NotesInfoList(notes=[
        {"notes_id": "1", "title": "Math Notes", "length": 120},
        {"notes_id": "2", "title": "Science Notes", "length": 150},
        {"notes_id": "3", "title": "History Notes", "length": 90}
    ]).dict()

@app.post("/generate_paper", response_model=PaperResponse)
def generate_paper(paper_format: PaperFormat):
    # Mock data for demonstration purposes
    mcqs = [
        {"question_no": 1, "question": "What is 2 + 2?", "options": ["3", "4", "5", "6"], "answer": "4"},
        {"question_no": 2, "question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": "Paris"}
    ]
    
    short_questions = [
        {"question_no": 1, "question": "Explain Newton's first law of motion.", "answer": "An object at rest stays at rest and an object in motion stays in motion unless acted upon by a net external force."}
    ]
    
    long_questions = [
        {"question_no": 1, "question": "Discuss the impact of World War II on Europe.", "answer": "World War II had a profound impact on Europe, leading to significant political, social, and economic changes."}
    ]
    
    return PaperResponse(
        paper_format=paper_format,
        mcqs=mcqs,
        short_questions=short_questions,
        long_questions=long_questions
    )
