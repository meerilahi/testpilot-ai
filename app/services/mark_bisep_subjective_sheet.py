from app.schemas.mark_bisep_subjective_sheet import MarkSubjectiveSheetRequest, MarkSubjectiveSheetResponse
from app.database.mongodb import get_answer_sheet
from app.core.extract_pages import extract_pages_from_pdf
from app.core.ocr_answer_sheet import ocr_answer_sheet
from app.core.mark_answer_sheet import mark_answer_sheet
from app.core.crop_answer_sheet import crop_pdf_pages
from app.core.filter_attempted import filter_attempted_questions

def mark_bisep_subjective_sheet_service(request :MarkSubjectiveSheetRequest)-> MarkSubjectiveSheetResponse:
    
    # get scanned answer sheet from database
    sheet_stream = get_answer_sheet("biology")
    print("Answer Sheet Retrived from database!")
    print("************************************")
    # crop answer sheet
    cropped_sheet_stream = crop_pdf_pages(sheet_stream,page_indices=list(range(3,30)),left=65,right=65,top=130,bottom=130)
    print("Answer Sheet cropped!")
    print("************************************")
    
    # extract answer pages from answer sheet
    images_dict = extract_pages_from_pdf(cropped_sheet_stream, request)
    print("Pages Extracted from pdf!")
    print("************************************")

    # ocr answers
    ocr_result = ocr_answer_sheet(images_dict)
    print("OCR Performed!")
    print("************************************")
    
    # filter attempted questions
    filter_qns = filter_attempted_questions(ocr_result)
    print("Attempted Questions Filtered!")
    print("************************************")

    # get rubric marks for each question
    mark_sheet = mark_answer_sheet(ocr_result, request, filter_qns)
    print("All Answer Sheet Marked!")
    print("************************************")

    # prepare response object
    response = MarkSubjectiveSheetResponse()
    
    # return response
    return None




request = MarkSubjectiveSheetRequest()

mark_bisep_subjective_sheet_service(request)