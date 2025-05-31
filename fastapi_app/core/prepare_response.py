from fastapi_app.schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetResponse, QuestionResponse,MarkSubjectiveAnswerSheetRequest
from typing import List, Dict, Any
import json
import base64
from io import BytesIO
import os
from typing import Dict, List
from PIL import Image

def prepare_response(mark_sheet, student_id, presentation_scores, request:MarkSubjectiveAnswerSheetRequest) -> MarkSubjectiveAnswerSheetResponse:
    question_responses = []

    for qn, mark_data in mark_sheet.items():
        rubrics_marks = mark_data.get("rubrics", [])
        marks_awarded = float(mark_data.get("marks", 0))
        feedback = mark_data.get("feedback", None)
        presentation_score = presentation_scores[qn]
        q_response = QuestionResponse(
            question_number=qn,
            rubrics_marks=rubrics_marks,
            presentation_score=presentation_score,
            feedback=feedback,
            total_marks=marks_awarded
        )
        question_responses.append(q_response)
    
    # rrq_qns = [question.question_number for question in request.list_of_questions if question.q_type == "rrq"]
    # erq_qns = [question.question_number for question in request.list_of_questions if question.q_type == "erq"]
    # rrq_question_responses = sorted([qn for qn in question_responses if qn in rrq_qns], key=lambda x:x.total_marks)[request.rrq_attempts-1]
    # erq_question_responses = sorted([qn for qn in question_responses if qn in erq_qns], key=lambda x:x.total_marks)[request.erq_attempts-1]
    # attempted_response = rrq_question_responses + erq_question_responses
    # total_marks_awarded = sum([res.total_marks for res in attempted_response])

    return MarkSubjectiveAnswerSheetResponse(
        student_id=student_id,
        list_of_attempted_questions=question_responses,
        total_paper_marks=0
    )


