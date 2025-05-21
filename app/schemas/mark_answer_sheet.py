from pydantic import BaseModel, Field
from typing import List, Annotated, Optional, Dict


class MCQ(BaseModel):
    number: Annotated[int, "MCQ number"]
    question: Annotated[int, "Question Text of MCQ"]
    options: Annotated[List[str], "Options of MCQ"]
    key: Annotated[List[str], "List of the correct options"]
    marks: Annotated[int, "Assigned marks to the question"]

class ShortQuestion(BaseModel):
    number: Annotated[int, "Question Number"] 
    question: Annotated[str, "Text of short question"]
    key: Annotated[List[str], "Answer Keys"]
    marks: Annotated[int, "Assigned marks to the question"]
    grammer_weight: Annotated[float, "The weightage of grammar in the question"]

class LongQuestion(BaseModel):
    number: Annotated[int, "Question Number"] 
    question: Annotated[str, "Text of Long question"]
    key: Annotated[str, "Answer Keys"]
    marks: Annotated[int, "Assigned marks to the question"]
    grammer_weight: Annotated[float, "The weightage of grammar in the question"]

class MarkAnswerSheetRequest(BaseModel):
    answer_sheed_id: Annotated[str, "Id of the answer sheet in database"]
    sectionA : Annotated[List[MCQ], "List of the MCQs"]
    sectionB : Annotated[List[ShortQuestion], "List of the short questions"]
    sectionC : Annotated[List[LongQuestion], "List of the long questions"]
    presentation_marks: Annotated[int, "Marks assigned to presentation"]



class MappedAnswers(BaseModel):
    sectionA : Annotated[List[Dict[int,str]], "List of dictionaries with question number as keys and student answer for mcqs as values"]
    sectionB : Annotated[List[Dict[int,str]], "List of dictionaries with question number as keys and student answer for short questions as values"]
    sectionC : Annotated[List[Dict[int,str]], "List of dictionaries with question number as keys and student answer for long questions as values"]



class MarkedAnswer(BaseModel):
    question_number: Annotated[int, "The question number"]
    marks: Annotated[int, "The marks awarded for the answer"]
    feedback: Annotated[Optional[str], "Feedback for the student"]

class MarkAnswerSheetResponse(BaseModel):
    id: Annotated[str, "The id of the answersheet"]
    sectionAMarks: Annotated[List[MarkedAnswer], "List of MCQs Marks"]
    sectionBMarks: Annotated[List[MarkedAnswer], "List of Short Question Marks"]
    sectionCMarks: Annotated[List[MarkedAnswer], "List of Long Question Marks"]
    mark_sheet: Annotated[List[MarkedAnswer], "List of marked answers"]
    total_marks: Annotated[int, "The total marks obtained by the student"]
    presentation_marks: Annotated[int, "The marks for presentation"]


