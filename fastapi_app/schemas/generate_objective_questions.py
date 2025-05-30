from pydantic import BaseModel
from typing import List, Dict, Tuple, Any,Annotated

class GenerateObjectiveQuestionsRequest(BaseModel):
    chapter_pages_dict: Annotated[Dict[int, Tuple[int, int]], "A dictionary in which keys are chapter numbers and values are range of pages in form of tuple"]
    mcqs_distribution: Annotated[Dict[int, Dict[str,int]], "A dictionary specifying number of MCQs to be generated for from each chapter. The value of is another dictionary with keys as difficulty levels and values as number of MCQs to be generated for that difficulty level"]

class GenerateObjectiveQuestionsResponse(BaseModel):
    mcqs_list: Annotated[List[Dict[str,Any]], "List of generated MCQs. Each question is represented as a dictionary with keys such as 'q_no', 'chapter_no', 'difficulty_level', 'question_text', 'options' and  'answer_key', ."]
