from app.schemas.mark_answer_sheet import MarkAnswerSheetRequest, MarkAnswerSheetResponse
from app.database.mongodb import get_answer_sheet
from app.core.mark_presentation import get_presentation_marks
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.output_parsers import RegexParser


def get_markdown(sheet):
    # llm    
    pass

def parse_markdown(markdown):
    # rules base
    pass

def align_markdown(markdown):
    # regular_expressions
    pass

def mark_answer(pair):
    # simarity
    pass




def mark_answer_sheet_service(request: MarkAnswerSheetRequest) -> MarkAnswerSheetResponse:
    sheet = get_answer_sheet("student_123")
    presentation_marks = get_presentation_marks(sheet)
    markdown = get_markdown(sheet)
    parsed_markdown = parse_markdown(markdown)
    aligned_markdown = align_markdown(parsed_markdown)

    pass