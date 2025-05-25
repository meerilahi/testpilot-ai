from PyPDF2 import PdfReader, PdfWriter
from io import BytesIO

def crop_pdf_pages(
    pdf_stream: BytesIO, 
    page_indices: list, 
    left: float, 
    right: float, 
    top: float, 
    bottom: float
) -> BytesIO:
    reader = PdfReader(pdf_stream)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        if i in page_indices:
            media_box = page.mediabox
            new_left = media_box.left + left
            new_bottom = media_box.bottom + bottom
            new_right = media_box.right - right
            new_top = media_box.top - top
            media_box.lower_left = (new_left, new_bottom)
            media_box.upper_right = (new_right, new_top)
        writer.add_page(page)
    output_stream = BytesIO()
    writer.write(output_stream)
    output_stream.seek(0)
    return output_stream


# with open("app/core/answer_sheet.pdf", "rb") as f:
#     input_stream = BytesIO(f.read())

# cropped_stream = crop_pdf_pages(
#     input_stream, 
#     page_indices=list(range(3,30)), 
#     left=65, 
#     right=65, 
#     top=130, 
#     bottom=130
# )

# # Save to file to inspect result
# with open("cropped_output.pdf", "wb") as f:
#     f.write(cropped_stream.getbuffer())

