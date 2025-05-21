from app.schemas.mark_answer_sheet import MarkAnswerSheetRequest, MarkAnswerSheetResponse
from app.database.mongodb import get_answer_sheet
from app.core.mark_presentation import get_presentation_marks
from app.core.pdf_to_markdown import pdf_to_markdown
from app.core.map_answers import map_answers



def get_marks(pairs):
    pass


def mark_answer_sheet_service(request: MarkAnswerSheetRequest) -> MarkAnswerSheetResponse:
    pdf_stream = get_answer_sheet("student_123")
    presentation_marks = get_presentation_marks(pdf_stream)
    markdown = pdf_to_markdown(pdf_stream)
    mapped_answers = map_answers(markdown, request)
    print(mapped_answers)
    return None


