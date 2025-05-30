from fastapi import FastAPI
from fastapi_app.services.mark_subjective_answersheet import mark_subjective_answersheet_service
from fastapi_app.services.generate_objective_questions import generate_objective_questions_service
from fastapi_app.schemas.generate_subjective_questions import GenerateSubjectiveQuestionsRequest, GenerateSubjectiveQuestionsResponse
from fastapi_app.services.generate_subjective_questions import generate_subjective_questions_service
from fastapi_app.schemas.generate_objective_questions import GenerateObjectiveQuestionsRequest, GenerateObjectiveQuestionsResponse
from fastapi_app.schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest, MarkSubjectiveAnswerSheetResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from io import BytesIO

app = FastAPI()

@app.post("/generate_objective_questions", response_model=GenerateObjectiveQuestionsResponse)
async def generate_objective_questions(
    data: str = Form(...),
    file: UploadFile = File(...)
) -> GenerateObjectiveQuestionsResponse:
    """
    Generate a objective questions based on the provided syllabus and requirements.
    """
    try:
        paperRequest = GenerateObjectiveQuestionsRequest.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON for request model: {e}")
    contents = await file.read()
    stream = BytesIO(contents)
    response = generate_objective_questions_service(paperRequest, stream)
    return response


@app.post("/generate_subjective_questions", response_model=GenerateSubjectiveQuestionsResponse)
async def generate_subjective_questions(
    data: str = Form(...),
    file: UploadFile = File(...)
) -> GenerateObjectiveQuestionsResponse:
    """
    Generate a subjective questions based on the provided syllabus and requirements.
    """
    try:
        paperRequest = GenerateSubjectiveQuestionsRequest.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON for request model: {e}")
    contents = await file.read()
    stream = BytesIO(contents)
    response = generate_subjective_questions_service(paperRequest, stream)
    return response




@app.post("/mark_subjective_answersheet", response_model=MarkSubjectiveAnswerSheetResponse)
async def mark_subjective_sheet(
    data: str = Form(...),
    file: UploadFile = File(...)
) -> MarkSubjectiveAnswerSheetResponse:
    """
    Mark the subjective answer sheet based on rubrics.
    """
    try:
        request = MarkSubjectiveAnswerSheetRequest.model_validate_json(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON for request model: {e}")
    contents = await file.read()
    stream = BytesIO(contents)
    response = mark_subjective_answersheet_service(request, stream)
    return response

