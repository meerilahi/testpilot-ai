from fastapi import FastAPI
from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from app.services.generate_question_paper import generate_question_paper_service
from app.schemas.mark_answer_sheet import MarkAnswerSheetRequest, MarkAnswerSheetResponse
from app.services.mark_answer_sheet import mark_answer_sheet_service

app = FastAPI()

@app.post("/generate_question_paper", response_model=GenerateQuestionPaperResponse)
async def generate_paper(paperRequest: GenerateQuestionPaperRequest) -> GenerateQuestionPaperResponse:
    """
    Generate a question paper based on the provided syllabus and requirements.
    """
    paperResponse = await generate_question_paper_service(paperRequest)
    return paperResponse

@app.post("/mark_answer_sheet")
async def mark_answer_sheet(request :MarkAnswerSheetRequest) -> MarkAnswerSheetResponse:
    """
    Mark the answer sheet based on the provided answer key and student answers.
    """
    mark_answer_sheet_service = await mark_answer_sheet_service(request)
    return mark_answer_sheet_service