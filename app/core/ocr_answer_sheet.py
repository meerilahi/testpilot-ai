from mistralai import Mistral
import os
from dotenv import load_dotenv
from mistralai import  ImageURLChunk
from app.database.mongodb import get_answer_sheet
from app.core.crop_answer_sheet import crop_pdf_pages
from app.core.extract_pages import extract_pages_from_pdf


load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def ocr_answer_sheet(images_dict):
    print("Performing OCR")    
    result = {}
    for index, page_images in images_dict.items():
        print(f'     Page {index} ---------')
        markdowns = []
        images = []
        result[index] = {}
        for image_encoded in page_images:
            base64_data_url = f"data:image/jpeg;base64,{image_encoded}"    
            response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
            markdowns.append(response_json['pages'][0]['markdown'])
            images = images + response_json['pages'][0]['images']
        '\n'.join(markdowns)
        result[index]['markdown'] = markdowns
        result[index]['images'] = images
    return result


# sheet =  get_answer_sheet("biology")

# print("Data Retrived from database")

# page_dict = {
#     1 : [0],
#     2 : [1],
#     3 : [2],
#     4 : [3],
#     5 : [4],
#     6 : [5],
#     7 : [6],
#     8 : [7],
#     9 : [8],
#     10 : [1],

# }
# images_dict = extract_pages_from_pdf(sheet, page_dict)
# print("Images extracted from pdf")
# ocr_result = ocr_answer_sheet(images_dict)
# print(ocr_result)






