from pydantic import BaseModel, Field
from typing import List, Annotated, Optional, Tuple

class QuestionRequest(BaseModel):
    question_number : Annotated[int, "Question Number"]
    q_type :Annotated[str, "Type of Question that is short or long"]
    question_text : Annotated[str, "Text of Question"]
    answer_key: Annotated[str, "Answer Key"]
    rubrics: Annotated[Optional[List[Tuple[str,float]]], "List of rubrics in form of tuples, first element of tuple is requirement while the second one is marks assigned for that requirement"]
    grammer_penalty: Annotated[str, "low, normal or high means how much should penalize grammetical mistakes."]
    question_marks: Annotated[float, "Total Marks for Question"]

class MarkSubjectiveAnswerSheetRequest(BaseModel):
    answerSheetPdfUrl : Annotated[str, "Pdf Url of the Answer Sheet"]
    list_of_questions: Annotated[List[QuestionRequest], "List of questions in subjective paper"]
    language: Annotated[str, "Language of Answer Sheet"]


class QuestionResponse(BaseModel):
    question_number : Annotated[int, "Question Number"]
    isAttempted: Annotated[bool, "True if the student attempt that question else false"]
    rubrics_marks: Annotated[Optional[List[Tuple[str,float]]], "List of marks awarded for each rubrics"]
    presentation_score: Annotated[Optional[float], "Higher if good presentation presentation of answer "]
    feedback: Annotated[Optional[str], "Feedback on answer"]
    total_marks: Annotated[Optional[float], "Total Marks awarded for Answer"]

class MarkSubjectiveAnswerSheetResponse(BaseModel):
    student_id: Annotated[int, "ID of Student"]
    list_of_evaluated_answers: Annotated[List[QuestionResponse], "List of evaluated answers"]


