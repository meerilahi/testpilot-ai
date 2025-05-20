from PIL import Image
import io
import os
from pdf2image import convert_from_path

def pdf_to_images(pdf_document):
    images = []
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap(dpi=800)
        image = Image.open(io.BytesIO(pix.tobytes("png")))
        images.append(image)
    return images

# from app.database.mongodb import get_answer_sheet
# pdf_doc = get_answer_sheet("student_123")
# images = pdf_to_images(pdf_doc)
# pix = images[0]
# pix.save("first_page_preview.png")
# print(f"PDF has {len(pdf_doc)} pages.")