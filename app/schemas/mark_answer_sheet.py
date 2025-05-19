from pydantic import BaseModel, Field
from typing import List, Dict, Tuple
from typing import Annotated, Optional


class Question(BaseModel):
    id: Annotated[str, "The unique identifier for the question"]
    number: Annotated[int, "The question number in the paper"]
    type: Annotated[str, "The type of question (e.g., MCQ, short answer, long answer)"]
    question: Annotated[str, "The question text"]
    options: Annotated[Optional[List[str]], "List of answer options for MCQs"]
    answerkey: Annotated[Optional[str], "The correct answer for the question"]
    marks : Annotated[int, "The marks assigned to the question"]
    grammer_weight: Annotated[float, "The weightage of grammar in the question"]

class AnswerSheet(BaseModel):
    pass

class MarkAnswerSheetRequest(BaseModel):
    questions: Annotated[List[Question], "List of questions in the question paper"]
    answer_sheet: Annotated[AnswerSheet, "The answer sheet to be marked"]



class MarkAnswerSheetResponse(BaseModel):
    pass
