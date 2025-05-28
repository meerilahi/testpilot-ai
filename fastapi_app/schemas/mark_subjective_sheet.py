from pydantic import BaseModel, Field
from typing import List, Annotated, Optional, Tuple

class QuestionRequest(BaseModel):
    question_number : Annotated[int, "Number of Question in question Paper"]
    pages : Annotated[List[int], "List of page number on answer sheet on which question is present"]
    q_type :Annotated[str, "Type of Question that is RRQ or ERQ"]
    question_text : Annotated[str, "Text of Question"]
    answer_key: Annotated[str, "Answer Key"]
    diagram_key: Annotated[Optional[str], Field(default=None), "Optional Base64 encoding of diagram if diagram is expected in answer"]
    rubrics: Annotated[Optional[List[Tuple[float,str]]], "List of rubrics, first number is marks while the second is requirement"]
    grammer_penalty: Annotated[str, "No, Low, Medium or High means how much should penalize grammetical mistakes."]
    question_marks: Annotated[float, "Total Marks for Question"]

class MarkSubjectiveSheetRequest(BaseModel):
    list_of_questions: Annotated[List[QuestionRequest], "List of questions in subjective paper"]
    rrq_attempts: Annotated[int, "Number of RRQ Questions to be attempted"]
    erq_attempts: Annotated[int, "Number of ERQ Questions to be attempted"]
    total_paper_marks : Annotated[float, "Total Marks of the subjective paper"]
    language: Annotated[str, "Language of Answer Sheet"]
    subject: Annotated[str, "Subject of Answer Sheet"]



class QuestionResponse(BaseModel):
    question_number : Annotated[int, "Number of Question in question Paper"]
    rubrics_marks: Annotated[List[Tuple[float,str]], "List of marks awarded for each rubrics"]
    presentation_score: Annotated[float, "Higher if good presentation presentation of answer "]
    feedback: Annotated[Optional[str], "Feedback on answer"]
    total_marks: Annotated[float, "Total Marks for Awarded for Answer"]

class MarkSubjectiveSheetResponse(BaseModel):
    list_of_questions: Annotated[List[QuestionResponse], "List of questions in questin marks"]
    total_paper_marks : Annotated[float, "Total Marks awarded to subjective answer sheet"]



