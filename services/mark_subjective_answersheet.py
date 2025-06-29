from PIL import Image
from io import BytesIO
from typing import List
from schemas.mark_subjective_answersheet import MarkSubjectiveAnswerSheetRequest, MarkSubjectiveAnswerSheetResponse, QuestionRequest
from pdf2image import convert_from_bytes
from core.extract_student_id import extract_student_id
from core.ocr_answer_sheet import ocr_answer_sheet
from core.mark_answer_sheet import mark_answer_sheet
from core.prepare_response import prepare_response
from core.presentation_score import get_presentation_score
from core.get_pdf_bytes_from_firebase import get_pdf_bytes_from_firebase
from core.pages_questions_mapping import map_pages_to_questions
from core.get_attempted_question_mask import get_attempted_question_mask
from core.pre_process_images import pre_process_images

def mark_subjective_answersheet_service(request :MarkSubjectiveAnswerSheetRequest)-> MarkSubjectiveAnswerSheetResponse:

    pdf_stream = BytesIO(get_pdf_bytes_from_firebase(request.answerSheetPdfUrl))
    print("✅ 1. PDF downloaded successfully")

    images : List[Image.Image] = convert_from_bytes(pdf_stream.read())
    print("✅ 2. Pages Extracted from PDF")

    student_id = extract_student_id(images[0])
    print(f"✅ 3. Student ID Extracted: {student_id}")

    images_dict = map_pages_to_questions(images)
    print("✅ 4. Pages mapped to question numbers")

    processed_images = pre_process_images(images_dict)
    print("✅ 5. Images pre-processed")

    ocr_result = ocr_answer_sheet(processed_images)
    print("✅ 6. OCR Performed")

    attempted_qns_mask = get_attempted_question_mask(ocr_result)
    print("✅ 7. Attempted Questions Filtered")
    print("Attempted Questions Mask:", attempted_qns_mask)

    presentation_scores = get_presentation_score(images_dict, attempted_qns_mask)
    print("✅ 9. Presentation assessed for all attempted questions")

    mark_sheet = mark_answer_sheet(ocr_result, request, attempted_qns_mask)
    print("✅ 10. All Answer Sheet Marked")

    response_model = prepare_response(mark_sheet, student_id, presentation_scores , request, attempted_qns_mask)
    print("✅ 11. Response Object generated from Marked Sheet")
        
    return response_model









