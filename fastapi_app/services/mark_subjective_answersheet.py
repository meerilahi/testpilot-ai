from PIL import Image
from typing import List
from io import BytesIO
from fastapi_app.schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest, MarkSubjectiveAnswerSheetResponse
from pdf2image import convert_from_bytes
from fastapi_app.core.extract_student_id import extract_student_id
from fastapi_app.core.identify_attempted_questions import identify_attempted_questions
from fastapi_app.core.filter_images import filter_images
from fastapi_app.core.crop_images import crop_images_in_dict
from fastapi_app.core.ocr_answer_sheet import ocr_answer_sheet
from fastapi_app.core.mark_answer_sheet import mark_answer_sheet
from fastapi_app.core.prepare_response import prepare_response
from fastapi_app.core.presentation_score import get_presentation_score


def mark_subjective_answersheet_service(request :MarkSubjectiveAnswerSheetRequest, pdf_stream : BytesIO)-> MarkSubjectiveAnswerSheetResponse:

    # extract pages from pdf
    images : List[Image.Image] = convert_from_bytes(pdf_stream.read())
    print("✅ 1. Images Extracted from PDF")

    # extract student id from first page
    student_id = extract_student_id(images[0])
    print(f"✅ 2. Student ID Extracted: {student_id}")

    # extract attempted questions
    attempted_qns = identify_attempted_questions(images[0])
    print(f"✅ 3. Attempted Questions Identified: {attempted_qns}")

    # filter images based on attempted questions
    images_dict = filter_images(images, attempted_qns, request)
    print("✅ 4. Images Filtered based on Attempted Questions")

    # crop images to remove header and footer
    images_dict = crop_images_in_dict(images_dict, left=65, top=130, right=65, bottom=130)
    print("✅ 5. Images Cropped to remove header and footer")

    # ocr answers
    ocr_result = ocr_answer_sheet(images_dict)
    print("✅ 6. OCR Performed")
    
    # get presentation scores for all questions
    presentation_scores = get_presentation_score(images_dict)
    print("✅ 7. Presentation assessed for all attempted questions")

    # get rubric marks for each question
    mark_sheet = mark_answer_sheet(ocr_result, request)
    print("✅ 8. All Answer Sheet Marked")

    # # prepare response object
    response_model = prepare_response(mark_sheet,presentation_scores, student_id, request)
    print("✅ 8. Response Object generated from Marked Sheet")
    
    return response_model





# def mark_subjective_answersheet_service(request :MarkSubjectiveAnswerSheetRequest, sheet_stream)-> MarkSubjectiveAnswerSheetResponse:


#     # crop answer sheet
#     cropped_sheet_stream = crop_pdf_pages(sheet_stream, page_indices=list(range(3,30)),left=65,right=65,top=130,bottom=130)
#     print("✅ 1. Answer Sheet cropped")
    
#     # extract answer pages from answer sheet
#     images_dict = extract_pages_from_pdf(cropped_sheet_stream, request)
#     print("✅ 2. Pages Extracted from pdf")

#     # ocr answers
#     ocr_result = ocr_answer_sheet(images_dict)
#     print("✅ 3. OCR Performed")
    
#     # filter attempted questions
#     attempted_qns = filter_attempted_questions(ocr_result)
#     print("✅ 4. Attempted Questions Filtered")

#     # get presentation scores for all questions
#     presentation_scores = get_presentation_score(images_dict, attempted_qns)
#     print("✅ 6. Presentation assessed for all attempted questions")

#     # get rubric marks for each question
#     mark_sheet = mark_answer_sheet(ocr_result, request, attempted_qns)
#     print("✅ 7. All Answer Sheet Marked")

#     # # prepare response object
    
#     response_model = convert_mark_sheet_to_response(mark_sheet,presentation_scores, request)
#     print("✅ 8. Response Object generated from Marked Sheet")
    
#     return response_model







