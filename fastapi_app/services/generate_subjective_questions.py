from io import BytesIO
from fastapi_app.schemas.generate_subjective_questions import GenerateSubjectiveQuestionsRequest, GenerateSubjectiveQuestionsResponse, QuestionResponse
from typing import List
from fastapi_app.core.generate_rrqs_erqs import generate_rrqs_erqs
from fastapi_app.core.extract_text_from_pages import extract_text_from_pages




def generate_subjective_questions_service(request: GenerateSubjectiveQuestionsRequest, book_stream: BytesIO) -> GenerateSubjectiveQuestionsResponse:
    
    all_generated_questions: List[QuestionResponse] = []
    
    print("Generating Subjective Question Paper")
    for chapter_no, page_range in request.chapter_pages_dict.items():
        
        chapter_questions = [q for q in request.question_list if q.chapter_no == chapter_no]

        if not chapter_questions:
            continue
        print(f"Generating subjective questions for chapter {chapter_no} with {len(chapter_questions)} questions")
        book_stream.seek(0)
        chapter_text = extract_text_from_pages(book_stream, page_range[0], page_range[1])
        questions =  generate_rrqs_erqs(chapter_questions, chapter_text)
        all_generated_questions.extend(questions)
    sorted_questions = sorted(all_generated_questions, key=lambda q: q.q_no)
    print("Subjective Question Paper Generated")
    return GenerateSubjectiveQuestionsResponse(list_of_question=sorted_questions)