from app.schemas.mark_bisep_subjective_sheet import MarkSubjectiveSheetRequest, MarkSubjectiveSheetResponse
from app.database.mongodb import get_answer_sheet
from app.core.extract_pages import extract_pages_from_pdf
from app.core.ocr_answer_sheet import ocr_answer_sheet





def mark_bisep_subjective_sheet_service(request :MarkSubjectiveSheetRequest)-> MarkSubjectiveSheetResponse:
    
    # get scanned answer sheet from database
    sheet = get_answer_sheet("taimoor")

    # extract answer pages from answer sheet
    page_dict = {q.question_number: q.pages for q in request.list_of_questions}
    images_dict = extract_pages_from_pdf(sheet, page_dict)

    # ocr each answer
    ocr_result = ocr_answer_sheet(images_dict)

    # get presentation score for each question

    # get grammer score for each question

    # get diagram marks for each question

    # get rubric marks for each question

    # get final marksheet

    
    pass