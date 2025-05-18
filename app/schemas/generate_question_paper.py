from pydantic import BaseModel, Field
from typing import List, Dict, Tuple
from typing import Annotated


class GenerateQuestionPaperRequest(BaseModel):
    notes_id: Annotated[str, "The Identifier of the notes from which the question paper is generated"]
    no_of_mcq: Annotated[int, "Number of multiple-choice questions"]
    no_of_short_questions: Annotated[int, "Number of short questions"]
    no_of_long_questions: Annotated[int, "Number of long questions"]
    difficulty_level: Annotated[str, "Difficulty level of the paper (e.g., easy, medium, hard)"]

class GenerateQuestionPaperResponse(BaseModel):
    mcqs: Annotated[List[Dict[str, object]], "List of multiple-choice questions with keys 'question', 'options', and 'answer'"]
    short_questions: Annotated[List[Dict[str, str]], "List of short questions paired with their answers"]
    long_questions: Annotated[List[Dict[str, str]], "List of long questions paired with their answers"]
