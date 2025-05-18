from fastapi import FastAPI
from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from app.services.generate_question_paper import generate_question_paper_service

app = FastAPI()

@app.post("/generate_question_paper", response_model=GenerateQuestionPaperResponse)
async def generate_paper(paperRequest: GenerateQuestionPaperRequest) -> GenerateQuestionPaperResponse:
    """
    Generate a question paper based on the provided syllabus and requirements.
    """
    paperResponse = await generate_question_paper_service(paperRequest)
    return paperResponse



@app.post("/mark_answer_sheet")
async def mark_answer_sheet():
    """
    Mark the answer sheet based on the provided answer key and student answers.
    """
    # Placeholder for marking answer sheet logic
    return {"message": "Answer sheet marked successfully."}