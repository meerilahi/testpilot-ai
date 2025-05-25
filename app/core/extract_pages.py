import base64
from io import BytesIO
import os
from typing import BinaryIO, Dict, List
from collections import defaultdict
from pdf2image import convert_from_bytes
from PIL import Image
from app.schemas.mark_bisep_subjective_sheet import MarkSubjectiveSheetRequest
from sample_request import sample_request
from app.database.mongodb import get_answer_sheet

def extract_pages_from_pdf(pdf_stream: BinaryIO, request: MarkSubjectiveSheetRequest ) -> Dict[int, List[str]]:
    page_dict = {q.question_number:  q.pages for q in request.list_of_questions}
    all_pages = convert_from_bytes(pdf_stream.read())
    result = defaultdict(list)
    for key, pages in page_dict.items():
        for page_num in pages:
            if 1 <= page_num <= len(all_pages):
                buffered = BytesIO()
                all_pages[page_num - 1].save(buffered, format="PNG")
                encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
                result[key].append(encoded_image)
            else:
                raise ValueError(f"Page number {page_num} is out of range. PDF has {len(all_pages)} pages.")

    return dict(result)

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
            print(f"Saved image for Question {question_num}, Page {i+1} at {image_path}")

# sheet =  get_answer_sheet("biology")

# base64_images = extract_pages_from_pdf(sheet, sample_request)

# for key, images in base64_images.items():
#     for img_b64 in images:
#         print(f"Image for key {key}:")
#         print(f"data:image/png;base64,{img_b64[:100]}...") 
