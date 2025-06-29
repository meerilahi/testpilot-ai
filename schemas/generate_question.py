from pydantic import BaseModel
from typing import List, Tuple
from typing import Annotated

class GenerateQuestionRequest(BaseModel):
    bookId : Annotated[str, "Id of the book in the KP text books"]
    chapter_no: Annotated[int, "Chapter Number from which question is to make"]
    q_type: Annotated[str, "Question Type that is short or long type"]
    difficulty_level: Annotated[str, "Difficulty level of Question that is Easy, Medium, Hard"]
    marks: Annotated[int, "Marks assigned for the question"]

class GenerateQuestionResponse(BaseModel):
    question_text: Annotated[str, "Text of the Generated Question"]
    answer_key: Annotated[str, "Answser key of the generated question"]
    rubrics: Annotated[List[Tuple[str, float]], "List of rubrics in form of list of tuples, the first element of tuple is the requirement that should be statisfied by student answer  and the second is the marks assigned for that rubric"]
