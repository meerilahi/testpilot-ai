from core.get_chapter_text import get_chapter_text
from core.generate_question import generate_question
from schemas.generate_question import GenerateQuestionRequest, GenerateQuestionResponse


def generate_question_service(request: GenerateQuestionRequest) -> GenerateQuestionResponse:
    print("Reading chapter text from markdown file:")
    text = get_chapter_text(request.bookTitle, request.chapter_no)
    print("Generating subjective question paper")
    question =  generate_question(request.q_type, request.difficulty_level, request.marks, text)
    return question
