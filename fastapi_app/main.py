from fastapi import FastAPI
from schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse
from services.generate_question_paper import generate_question_paper_service
from services.mark_subjective_sheet import mark_subjective_sheet_service
from schemas.mark_subjective_sheet import MarkSubjectiveSheetRequest, MarkSubjectiveSheetResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from io import BytesIO

app = FastAPI()

@app.post("/generate_question_paper", response_model=GenerateQuestionPaperResponse)
async def generate_paper(
    data: str = Form(...),
    file: UploadFile = File(...)
) -> GenerateQuestionPaperResponse:
    """
    Generate a question paper based on the provided syllabus and requirements.
    """
    try:
        paperRequest = GenerateQuestionPaperRequest.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON for request model: {e}")
    contents = await file.read()
    stream = BytesIO(contents)
    response = generate_question_paper_service(paperRequest, stream)
    return response



@app.post("/mark_bisep_subjective", response_model=MarkSubjectiveSheetResponse)
async def mark_subjective_sheet(
    data: str = Form(...),
    file: UploadFile = File(...)
) -> MarkSubjectiveSheetResponse:
    """
    Mark the subjective answer sheet based on rubrics.
    """
    try:
        request = MarkSubjectiveSheetRequest.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON for request model: {e}")
    contents = await file.read()
    stream = BytesIO(contents)
    response = mark_subjective_sheet_service(request, stream)
    return response