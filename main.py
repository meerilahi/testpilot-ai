from fastapi import FastAPI
from schemas.generate_mcq import GenerateMCQRequest, GenerateMCQResponse
from services.generate_mcq_service import generate_MCQ_service
from services.mark_subjective_answersheet import mark_subjective_answersheet_service
from schemas.generate_question import GenerateQuestionRequest, GenerateQuestionResponse
from services.generate_questions import generate_question_service
from schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest, MarkSubjectiveAnswerSheetResponse
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_mcq", response_model=GenerateMCQResponse)
async def generate_mcq( request: GenerateMCQRequest) -> GenerateMCQResponse:
    """
    Generate a MCQ based on the provided chapter number, difficulty level, and bookId.
    """
    try:
        response = generate_MCQ_service(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating MCQ: {e}")

@app.post("/generate_question", response_model=GenerateQuestionResponse)
async def generate_question(
    request: GenerateQuestionRequest
) -> GenerateQuestionRequest:
    """
    Generate a subjective question based on the provided requirements and bookId.
    """
    try:
        response = generate_question_service(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating Question: {e}")
    return response

@app.post("/mark_subjective_answersheet", response_model=MarkSubjectiveAnswerSheetResponse)
async def mark_subjective_sheet(
    request: MarkSubjectiveAnswerSheetRequest
) -> MarkSubjectiveAnswerSheetResponse:
    """
    Mark the subjective answer sheet based on rubrics.
    """
    try:
        response = mark_subjective_answersheet_service(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error marking Sheet: {e}")
    return response


