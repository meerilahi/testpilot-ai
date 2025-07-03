from pydantic import BaseModel
from typing import List, Annotated

class GenerateMCQRequest(BaseModel):
    bookTitle : Annotated[str, "Title of the book in the KP text books"]
    chapter_number : Annotated[int, "Chapter number for which MCQs are to be generated"]
    difficulty_level: Annotated[str, "Difficulty level of the MCQs to be generated. It can be 'easy', 'medium', or 'hard'"]

class GenerateMCQResponse(BaseModel):
    question : Annotated[str, "The generated MCQ question text"]
    options: Annotated[List[str], "List of options for the MCQ question"]
    correct_option_index: Annotated[int, "The index correct option for the MCQ question"]