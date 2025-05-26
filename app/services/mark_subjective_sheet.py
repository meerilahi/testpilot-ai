from app.schemas.mark_subjective_sheet import MarkSubjectiveSheetRequest, MarkSubjectiveSheetResponse
from app.core.extract_pages import extract_pages_from_pdf
from app.core.ocr_answer_sheet import ocr_answer_sheet
from app.core.mark_answer_sheet import mark_answer_sheet
from app.core.crop_answer_sheet import crop_pdf_pages
from app.core.filter_attempted import filter_attempted_questions
from app.core.prepare_response import convert_mark_sheet_to_response



def mark_subjective_sheet_service(request :MarkSubjectiveSheetRequest, sheet_stream)-> MarkSubjectiveSheetResponse:

    # crop answer sheet
    cropped_sheet_stream = crop_pdf_pages(sheet_stream, page_indices=list(range(3,30)),left=65,right=65,top=130,bottom=130)
    print("✅ 1. Answer Sheet cropped")
    
    # extract answer pages from answer sheet
    images_dict = extract_pages_from_pdf(cropped_sheet_stream, request)
    print("✅ 2. Pages Extracted from pdf")

    # ocr answers
    ocr_result = ocr_answer_sheet(images_dict)
    print("✅ 3. OCR Performed")
    
    # filter attempted questions
    filter_qns = filter_attempted_questions(ocr_result)
    print("✅ 4. Attempted Questions Filtered")

    # get rubric marks for each question
    mark_sheet = mark_answer_sheet(ocr_result, request, filter_qns)
    print("✅ 5. All Answer Sheet Marked")

    # # prepare response object
    response_model = convert_mark_sheet_to_response(mark_sheet)
    print("✅ 6. Response Object generated from Marked Sheet")
    
    return response_model








