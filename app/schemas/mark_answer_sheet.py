from pydantic import BaseModel, Field
from typing import List, Dict, Tuple
from typing import Annotated, Optional


class QuestionRubic(BaseModel):
    number: Annotated[int, "The question number in the paper"]
    type: Annotated[str, "The type of question (e.g., MCQ, short answer, long answer)"]
    question: Annotated[str, "The question text"]
    options: Annotated[Optional[List[str]], "List of answer options for MCQs"]
    answerkey: Annotated[Optional[str], "The correct answer for the question"]
    marks : Annotated[int, "The marks assigned to the question"]
    grammer_weight: Annotated[float, "The weightage of grammar in the question"]

class MarkAnswerSheetRequest(BaseModel):
    questions_rubic: Annotated[List[QuestionRubic], "List of questions in the question paper"]
    id: Annotated[str, "The id of answersheet to be marked"]



class MarkedAnswer(BaseModel):
    question_number: Annotated[int, "The question number in the paper"]
    marks: Annotated[int, "The marks awarded for the answer"]
    feedback: Annotated[Optional[str], "Feedback for the student"]

class MarkAnswerSheetResponse(BaseModel):
    id: Annotated[str, "The id of the answersheet"]
    mark_sheet: Annotated[List[MarkedAnswer], "List of marked answers"]
    total_marks: Annotated[int, "The total marks obtained by the student"]
    presentation_marks: Annotated[int, "The marks for presentation"]
