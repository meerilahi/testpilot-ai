from core.get_chapter_text import get_chapter_text
from schemas.generate_mcq import GenerateMCQRequest, GenerateMCQResponse
from core.generate_mcq import generate_mcq

map = {
    'A' : 0,
    'B' : 1,
    'C' : 2,
    'D' : 3
}

def generate_MCQ_service(request: GenerateMCQRequest) -> GenerateMCQResponse:
    print("Reading chapter text from markdown file:")
    text = get_chapter_text(request.bookTitle, request.chapter_number)
    print("Generating MCQ:")
    mcq = generate_mcq(request.difficulty_level, text)
    return GenerateMCQResponse(
        question=mcq["question_text"],
        options=mcq["options"],
        correct_option_index=map[mcq["answer_key"]]
    )