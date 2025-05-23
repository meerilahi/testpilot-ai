from fastapi import FastAPI
from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from app.services.generate_question_paper import generate_question_paper_service
from app.schemas.mark_answer_sheet import MarkAnswerSheetRequest, MarkAnswerSheetResponse
from app.services.mark_answer_sheet import mark_answer_sheet_service
from app.core.pdf_to_markdown import pdf_to_markdown
from app.database.mongodb import get_answer_sheet

app = FastAPI()

@app.post("/generate_question_paper", response_model=GenerateQuestionPaperResponse)
async def generate_paper(paperRequest: GenerateQuestionPaperRequest) -> GenerateQuestionPaperResponse:
    """
    Generate a question paper based on the provided syllabus and requirements.
    """
    response = await generate_question_paper_service(paperRequest)
    return response

@app.post("/mark_answer_sheet")
async def mark_answer_sheet(request :MarkAnswerSheetRequest) -> MarkAnswerSheetResponse:
    """
    Mark the answer sheet based on the provided answer key and student answers.
    """
    response = await mark_answer_sheet_service(request)
    return response

sheet = get_answer_sheet("taimoor")
markdown = pdf_to_markdown(sheet)
print(markdown)
with open("output.md", "w", encoding="utf-8") as f:
    f.write(markdown)