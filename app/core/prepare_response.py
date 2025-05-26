from app.schemas.mark_subjective_sheet import MarkSubjectiveSheetResponse, QuestionResponse,MarkSubjectiveSheetRequest
from typing import List, Dict, Any
import json
import base64
from io import BytesIO
import os
from typing import Dict, List
from PIL import Image

def convert_mark_sheet_to_response(mark_sheet, presentation_scores, request:MarkSubjectiveSheetRequest) -> MarkSubjectiveSheetResponse:
    question_responses = []

    for qn, mark_data in mark_sheet.items():
        rubrics_marks = mark_data.get("rubrics", [])
        marks_awarded = float(mark_data.get("marks", 0))
        feedback = mark_data.get("feedback", None)
        presentation_score = presentation_scores[qn]
        q_response = QuestionResponse(
            question_number=qn,
            rubrics_marks=rubrics_marks,
            presentation_score=presentation_score,
            feedback=feedback,
            total_marks=marks_awarded
        )
        question_responses.append(q_response)
    
    # rrq_qns = [question.question_number for question in request.list_of_questions if question.q_type == "rrq"]
    # erq_qns = [question.question_number for question in request.list_of_questions if question.q_type == "erq"]
    # rrq_question_responses = sorted([qn for qn in question_responses if qn in rrq_qns], key=lambda x:x.total_marks)[request.rrq_attempts-1]
    # erq_question_responses = sorted([qn for qn in question_responses if qn in erq_qns], key=lambda x:x.total_marks)[request.erq_attempts-1]
    # attempted_response = rrq_question_responses + erq_question_responses
    # total_marks_awarded = sum([res.total_marks for res in attempted_response])

    return MarkSubjectiveSheetResponse(
        list_of_questions=question_responses,
        total_paper_marks=0
    )



# def save_mark_sheet_to_json(mark_sheet: Dict[str, Any], filename: str = "mark_sheet.json") -> None:
#     with open(filename, "w", encoding="utf-8") as f:
#         json.dump(mark_sheet, f, indent=2, ensure_ascii=False)

# def save_mark_sheet_to_markdown(mark_sheet: Dict[str, Any], filename: str = "mark_sheet.md") -> None:
#     lines = ["# Mark Sheet\n"]
#     for question_number, result in mark_sheet.items():
#         lines.append(f"## Question {question_number}\n")
#         lines.append(f"**Total Marks Awarded:** {result['marks']}\n")
#         lines.append("### Rubric Evaluation:\n")
#         for i, (awarded, justification) in enumerate(result['rubrics'], 1):
#             lines.append(f"- **Point {i}:** {awarded} marks — {justification}")
#         lines.append("\n### Feedback:\n")
#         lines.append(f"{result['feedback']}\n")
#         lines.append("---\n")
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write("\n".join(lines))


# def write_ocr_to_markdown(ocr_result: dict, output_dir: str):
#     os.makedirs(output_dir, exist_ok=True)
#     for question_number, content in ocr_result.items():
#         question_dir = os.path.join(output_dir, f"question_{question_number}")
#         os.makedirs(question_dir, exist_ok=True)
#         markdown_lines = content.get("markdown", [])
#         markdown_content = "\n\n".join(markdown_lines)
#         img_data = content.get('image')
#         if img_data:
#             image_path = os.path.join(question_dir, 'diagram.png')
#             with open(image_path, "wb") as img_file:
#                 img_file.write(base64.b64decode(img_data))
#             markdown_content += f"\n\n![Image](diagram.png)"
#         markdown_file_path = os.path.join(question_dir, f"question_{question_number}.md")
#         with open(markdown_file_path, "w", encoding="utf-8") as md_file:
#             md_file.write(markdown_content)

# def save_images_from_dict(images_dict: Dict[int, List[str]], save_dir: str) -> None:
#     os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist
#     for question_num, images in images_dict.items():
#         question_dir = os.path.join(save_dir, f"question_{question_num}")
#         os.makedirs(question_dir, exist_ok=True)
#         for i, encoded_img in enumerate(images):
#             img_data = base64.b64decode(encoded_img)
#             image = Image.open(BytesIO(img_data))
#             image_path = os.path.join(question_dir, f"page_{i+1}.png")
#             image.save(image_path)


