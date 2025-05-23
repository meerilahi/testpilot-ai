from pydantic import BaseModel
from typing import List, Annotated, Optional, Tuple

class QuestionRequest(BaseModel):
    question_number : Annotated[int, "Number of Question in question Paper"]
    pages : Annotated[List[int], "List of page number on answer sheet on which question is present"]
    question_text : Annotated[List[int], "Text of Question"]
    answer_key: Annotated[Optional[str], "Answer Key"]
    is_comprehensive: Annotated[bool, "True for long question answers and false for the opposite case"]
    rubrics: Annotated[Optional[List[Tuple[int,str]]], "List of rubrics"]
    presentation_weightage: Annotated[int, "Weightage for bad presentation of answer"]
    grammer_weightage: Annotated[float, "Weightage for grammetical mistakes in answer"]
    diagram_key: Annotated[Optional[str], "Optional Base64 encoding of diagram if diagram is expected in answer"]
    diagram_marks: Annotated[Optional[int], "Optional Marks for diagram if diagram is expected in the answer"]
    total_marks: Annotated[int, "Total Marks for Question"]

class MarkSubjectiveSheetRequest(BaseModel):
    list_of_questions: Annotated[List[QuestionRequest], "List of questions in subjective paper"]
    total_paper_marks = Annotated[int, "Total Marks of the subjective paper"]
    answer_sheet_id: Annotated[str, "Id of answer sheet in database"]
    language: Annotated[str, "Language of Answer Sheet"]
    subject: Annotated[str, "Subject of Answer Sheet"]


class QuestionResponse(BaseModel):
    question_number : Annotated[int, "Number of Question in question Paper"]
    rubrics_marks: Annotated[List[Tuple[int,str]], "List of marks awarded for each rubrics"]
    presentation_score: Annotated[int, "Higher if good presentation presentation of answer "]
    grammer_score: Annotated[float, "Higher if good presentation presentation of answer"]
    diagram_marks: Annotated[Optional[int], "Marks awarded for diagram"]
    total_marks: Annotated[int, "Total Marks for Awarded for Answer"]


class MarkSubjectiveSheetResponse(BaseModel):
    list_of_questions: Annotated[List[QuestionResponse], "List of questions in questin marks"]
    total_paper_marks = Annotated[int, "Total Marks awarded to subjective answer sheet"]