from PIL import Image
from typing import List, Dict
from fastapi_app.schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest

def filter_images(images : List[Image.Image], attempted_qns: List[int], request : MarkSubjectiveAnswerSheetRequest) -> Dict[int, List[Image.Image]]:
    pages_dict = {qns.question_number: qns.pages for qns in request.list_of_questions}
    result = {}
    for qns in attempted_qns:
        result[qns] = [ images[page - 1] for page in pages_dict[qns] if page - 1 < len(images) ]
    return result
