from pdf2image import convert_from_bytes
from typing import List
from PIL import Image
from io import BytesIO

with open("/home/taimoor/Repositories/testpilot-ai/temp_data/sample_answer_sheet.pdf", "rb") as f:
    stream = BytesIO(f.read())

images = convert_from_bytes(stream.read())


images[5].show()
