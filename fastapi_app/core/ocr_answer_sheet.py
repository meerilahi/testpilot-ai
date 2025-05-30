from mistralai import Mistral
import os
import base64
from dotenv import load_dotenv
from mistralai import  ImageURLChunk
from fastapi_app.core.merge_images import combine_base64_images
from fastapi_app.core.encode_images import encode_images_to_base64
from io import BytesIO

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def ocr_answer_sheet(images_dict):
    encoded_dict = encode_images_to_base64(images_dict)
    result = {}
    for qn, page_images in encoded_dict.items():
        markdowns = []
        images = []
        result[qn] = {}
        for image_encoded in page_images:
            base64_data_url = f"data:image/jpeg;base64,{image_encoded}"    
            response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
            markdowns.append(response_json['pages'][0]['markdown'])
            images = images + [image_obj["image_base64"]  for image_obj in response_json['pages'][0]['images']]
        result[qn]['markdown'] = '\n'.join(markdowns)
        result[qn]['image'] = combine_base64_images(images)
    return result







