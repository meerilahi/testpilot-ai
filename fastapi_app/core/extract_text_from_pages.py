from PyPDF2 import PdfReader

def extract_text_from_pages(pdf_stream, start_page: int, end_page: int) -> str:
    reader = PdfReader(pdf_stream)
    text = ""
    for i in range(start_page - 1, end_page):
        if i < len(reader.pages):
            text += reader.pages[i].extract_text() or ""
    return text