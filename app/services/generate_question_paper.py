from app.schemas.generate_question_paper import GenerateQuestionPaperRequest, GenerateQuestionPaperResponse,QuestionRequest, QuestionResponse
from PyPDF2 import PdfReader
from typing import List
from app.core.generate_questions_from_chapter_text import generate_questions_from_chapter_text

def extract_text_from_pages(pdf_stream, start_page: int, end_page: int) -> str:
    reader = PdfReader(pdf_stream)
    text = ""
    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            text += reader.pages[i].extract_text() or ""
    return text


def generate_question_paper_service(request: GenerateQuestionPaperRequest, book_stream) -> GenerateQuestionPaperResponse:
    all_generated_questions: List[QuestionResponse] = []
    print("Generating Question Paper",flush=True)
    for chapter_no, page_range in request.chapter_pages_dict.items():
        
        chapter_questions = [q for q in request.question_list if q.chapter_no == chapter_no]

        if not chapter_questions:
            continue 
        book_stream.seek(0)
        chapter_text = extract_text_from_pages(book_stream, page_range[0], page_range[1])
        questions =  generate_questions_from_chapter_text(chapter_questions, chapter_text)
        print(f"Questions Generated from chapter {chapter_no}")
        all_generated_questions.extend(questions)
    sorted_questions = sorted(all_generated_questions, key=lambda q: q.q_no)
    print("Question Paper Generated")
    return GenerateQuestionPaperResponse(list_of_question=sorted_questions)