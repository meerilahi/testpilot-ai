from fastapi import FastAPI
from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from app.services.generate_question_paper import generate_question_paper_service
from app.services.mark_bisep_subjective_sheet import mark_bisep_subjective_sheet_service
from app.schemas.mark_bisep_subjective_sheet import MarkSubjectiveSheetRequest, MarkSubjectiveSheetResponse
from temp_data.sample_request import sample_request

app = FastAPI()

@app.post("/generate_question_paper", response_model=GenerateQuestionPaperResponse)
async def generate_paper(paperRequest: GenerateQuestionPaperRequest) -> GenerateQuestionPaperResponse:
    """
    Generate a question paper based on the provided syllabus and requirements.
    """
    response = await generate_question_paper_service(paperRequest)
    return response

@app.post("/mark_bisep_subjective")
async def mark_answer_sheet(request :MarkSubjectiveSheetRequest) -> MarkSubjectiveSheetResponse:
    """
    Mark the Bisep style subjective answer sheet based on rubrics.
    """
    response = await mark_bisep_subjective_sheet_service(request)
    return response

sample_response = mark_answer_sheet(sample_request)