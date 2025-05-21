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