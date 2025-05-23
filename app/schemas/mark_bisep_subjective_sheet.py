from pydantic import BaseModel
from typing_extensions import List, Annotated, Optional, Tuple

class QuestionRequest(BaseModel):
    question_number : Annotated[int, "Number of Question in question Paper"]
    pages : Annotated[List[int], "List of page number on answer sheet on which question is present"]
    section :Annotated[str, "section B or C"]
    question_text : Annotated[List[int], "Text of Question"]
    answer_key: Annotated[Optional[str], "Answer Key"]
    diagram_key: Annotated[Optional[str], "Optional Base64 encoding of diagram if diagram is expected in answer"]
    rubrics: Annotated[Optional[List[Tuple[int,str]]], "List of rubrics, first number is marks while the second is criteria"]
    presentation_weightage: Annotated[int, "Weightage for bad presentation of answer"]
    grammer_weightage: Annotated[float, "Weightage for grammetical mistakes in answer"]
    question_marks: Annotated[int, "Total Marks for Question"]


# q1 = QuestionRequest(
#     question_number = 1,
#     pages = [1,2]
#     section "B"
#     question_text =  "Complete the organization level against each example : \n Examples Stomach \n Man \n Glucose \n Ribosome"
#     answer_key = " Examples \t Organization Level \n Stomach \t Organ \n Man \t Organism \n Glucose \t Molecule \n Ribosome \t"
#     diagram_key = None
#     rubrics: [()]
#     presentation_weightage: Annotated[int, "Weightage for bad presentation of answer"]
#     grammer_weightage: Annotated[float, "Weightage for grammetical mistakes in answer"]
#     question_marks: Annotated[int, "Total Marks for Question"]
# )

class MarkSubjectiveSheetRequest(BaseModel):
    list_of_questions: Annotated[List[QuestionRequest], "List of questions in subjective paper"]
    sectionB_questions: Annotated[int, "Number of Question to be attempted in Section B"]
    sectionC_questions: Annotated[int, "Number of Question to be attempted in Section C"]
    total_paper_marks : Annotated[int, "Total Marks of the subjective paper"]
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
    total_paper_marks : Annotated[int, "Total Marks awarded to subjective answer sheet"]
    
    
