from pydantic import BaseModel
from typing import List, Tuple, Optional
from pydantic import Field

class PaperFormat(BaseModel):
    notes_id: str
    page_ranges: List[str]
    no_of_mcqs: int
    no_of_short_answers: int
    no_of_long_answers: int
    difficulty_level: str = Field(..., regex="^(easy|medium|hard)$")

class MCQ(BaseModel):
    question_no : int
    question: str
    options: List[str]
    answer: str

class ShortQuestion(BaseModel):
    question_no: int
    question: str
    answer: str

class LongQuestion(BaseModel):
    question_no: int
    question: str
    answer: str

class PaperResponse(BaseModel):
    paper_format: PaperFormat
    mcqs: List[MCQ]
    short_questions: List[ShortQuestion]
    long_questions: List[LongQuestion]
