import base64
from io import BytesIO
import os
from typing import BinaryIO, Dict, List
from collections import defaultdict
from pdf2image import convert_from_bytes
from PIL import Image
from schemas.mark_subjective_sheet import MarkSubjectiveSheetRequest

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
