from pydantic import BaseModel
from typing import List, Tuple, Optional
from pydantic import Field

class NotesInfo(BaseModel):
    notes_id: str
    title: str
    length: int 

class NotesInfoList(BaseModel):
    notes: List[NotesInfo]

class PaperFormat(BaseModel):
    no_of_mcqs: int
    no_of_short_answers: int
    no_of_long_answers: int
    difficulty_level: str = Field(..., regex="^(easy|medium|hard)$")

class PaperRequest(BaseModel):
    notes_id: str
    page_ranges: List[str]
    paper_format: PaperFormat



class PaperResponse(BaseModel):
    mcqs: List[Tuple[str, List[str]]]
    short_questions: List[str]
    long_questions: List[str]


