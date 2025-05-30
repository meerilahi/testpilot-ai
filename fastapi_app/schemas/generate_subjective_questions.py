
from pydantic import BaseModel
from typing import List, Dict, Tuple
from typing import Annotated


class QuestionRequest(BaseModel):
    q_no: Annotated[int, "Question Number in Question Paper"]
    q_type: Annotated[str, "Question Type that is short or long answer type"]
    chapter_no: Annotated[int, "Chapter Number from which question is to make"]
    difficulty_level: Annotated[str, "Difficulty level of Question that is Easy, Medium, Hard"]
    marks: Annotated[int, "Marks assigned for the question"]

class GenerateSubjectiveQuestionsRequest(BaseModel):
    chapter_pages_dict: Annotated[Dict[int, Tuple[int,int]], "A dictionary in which keys are chapter numbers and values are range of pages in form of tuple"]
    question_list: Annotated[List[QuestionRequest], "List of Questions to be generated"]



class QuestionResponse(BaseModel):
    q_no: Annotated[int, "Question Number in Question Paper"]
    q_type: Annotated[str, "Question Type that is short or long answer type"]
    chapter_no: Annotated[int, "Chapter Number from which question is to make"]
    difficulty_level: Annotated[str, "Difficulty level of Question that is Easy, Medium, Hard"]
    marks: Annotated[float, "Marks assigned for the question"]
    question_text: Annotated[str, "Text of the Generated Question"]
    answer_key: Annotated[str, "Answser key of the generated question"]
    rubrics: Annotated[List[Tuple[float, str]], "List of rubrics in form of list of tuples, the first element of tuple is marks assigned and the second is the requirement statisfied by student answer for that marks"]

class GenerateSubjectiveQuestionsResponse(BaseModel):
    list_of_question: Annotated[List[QuestionResponse], "List of Generated Questions"]
