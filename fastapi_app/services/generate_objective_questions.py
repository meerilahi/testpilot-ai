from fastapi_app.schemas.generate_objective_questions import GenerateObjectiveQuestionsRequest, GenerateObjectiveQuestionsResponse
from io import BytesIO
from fastapi_app.core.extract_text_from_pages import extract_text_from_pages
from typing import List, Dict, Any
from fastapi_app.core.generate_mcq import generate_mcq



def generate_objective_questions_service( request : GenerateObjectiveQuestionsRequest, stream : BytesIO) -> GenerateObjectiveQuestionsResponse:
     mcq_list : List[Dict[str,Any]] = []
     print("Generating Objective Question Paper")
     for chapter_no, page_range in request.chapter_pages_dict.items():
          chapter_text = extract_text_from_pages(stream, page_range[0], page_range[1])
          mcqs_distribution = request.mcqs_distribution.get(chapter_no, {})
          print(f"Generating MCQs for chapter {chapter_no}")
          for difficulty_level, num_mcqs in mcqs_distribution.items():
               for _ in range(num_mcqs):
                    mcq = generate_mcq(difficulty_level, chapter_text)
                    mcq_list.append({
                         "q_no": len(mcq_list) + 1,
                         "chapter_no": chapter_no,
                         "difficulty_level": difficulty_level,
                         "question_text": mcq["question_text"],
                         "options": mcq["options"],
                         "answer_key": mcq["answer_key"]
                    })
     print("Objective Question Paper Generated")
     return GenerateObjectiveQuestionsResponse(mcqs_list=mcq_list)