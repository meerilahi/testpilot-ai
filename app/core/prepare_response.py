from app.schemas.mark_bisep_subjective_sheet import MarkSubjectiveSheetResponse, QuestionResponse
from typing import List, Dict, Any
import json
import base64
from io import BytesIO
import os
from typing import Dict, List
from PIL import Image

def save_mark_sheet_to_json(mark_sheet: Dict[str, Any], filename: str = "mark_sheet.json") -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mark_sheet, f, indent=2, ensure_ascii=False)

def save_mark_sheet_to_markdown(mark_sheet: Dict[str, Any], filename: str = "mark_sheet.md") -> None:
    lines = ["# Mark Sheet\n"]
    for question_number, result in mark_sheet.items():
        lines.append(f"## Question {question_number}\n")
        lines.append(f"**Total Marks Awarded:** {result['marks']}\n")
        lines.append("### Rubric Evaluation:\n")
        for i, (awarded, justification) in enumerate(result['rubrics'], 1):
            lines.append(f"- **Point {i}:** {awarded} marks — {justification}")
        lines.append("\n### Feedback:\n")
        lines.append(f"{result['feedback']}\n")
        lines.append("---\n")
    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def convert_mark_sheet_to_response(mark_sheet: Dict[str, Any]) -> MarkSubjectiveSheetResponse:
    questions: List[QuestionResponse] = []
    for qn_str, data in mark_sheet.items():
        question_number = int(qn_str)
        question_response = QuestionResponse(
            question_number=question_number,
            rubrics_marks=data["rubrics"],
            feedback=data["feedback"],
            presentation_score=data.get("presentation_score", 0),
            grammer_score=data.get("grammer_score", 0.0),
            total_marks=data["marks"]
        )
        questions.append(question_response)
    total_paper_marks = sum(q.total_marks for q in questions)
    return MarkSubjectiveSheetResponse(
        list_of_questions=questions,
        total_paper_marks=total_paper_marks
    )


def write_ocr_to_markdown(ocr_result: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for question_number, content in ocr_result.items():
        question_dir = os.path.join(output_dir, f"question_{question_number}")
        os.makedirs(question_dir, exist_ok=True)
        markdown_lines = content.get("markdown", [])
        markdown_content = "\n\n".join(markdown_lines)
        img_data = content.get('image')
        if img_data:
            image_path = os.path.join(question_dir, 'diagram.png')
            with open(image_path, "wb") as img_file:
                img_file.write(base64.b64decode(img_data))
            markdown_content += f"\n\n![Image](diagram.png)"
        markdown_file_path = os.path.join(question_dir, f"question_{question_number}.md")
        with open(markdown_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

def save_images_from_dict(images_dict: Dict[int, List[str]], save_dir: str) -> None:
    os.makedirs(save_dir, exist_ok=True)  # Create directory if it doesn't exist
    for question_num, images in images_dict.items():
        question_dir = os.path.join(save_dir, f"question_{question_num}")
        os.makedirs(question_dir, exist_ok=True)
        for i, encoded_img in enumerate(images):
            img_data = base64.b64decode(encoded_img)
            image = Image.open(BytesIO(img_data))
            image_path = os.path.join(question_dir, f"page_{i+1}.png")
            image.save(image_path)