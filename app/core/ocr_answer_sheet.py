from mistralai import Mistral
import os
import base64
from dotenv import load_dotenv
from mistralai import  ImageURLChunk

load_dotenv()

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

def ocr_answer_sheet(images_dict):
    print("Performing OCR")    
    result = {}
    for qn, page_images in images_dict.items():
        if qn in [6,7,8,9,10,11,12,13]:
            continue
        print(f'     Question No. {qn} ---------')
        markdowns = []
        images = []
        result[qn] = {}
        for image_encoded in page_images:
            base64_data_url = f"data:image/jpeg;base64,{image_encoded}"    
            response_json = client.ocr.process(document=ImageURLChunk(image_url=base64_data_url), model="mistral-ocr-latest").model_dump()
            markdowns.append(response_json['pages'][0]['markdown'])
            images = images + [image_obj["image_base64"]  for image_obj in response_json['pages'][0]['images']]
            # print(response_json['pages'][0])
        '\n'.join(markdowns)
        result[qn]['markdown'] = markdowns
        result[qn]['images'] = images

        
    return result


def write_ocr_to_markdown(ocr_result: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for question_number, content in ocr_result.items():
        question_dir = os.path.join(output_dir, f"question_{question_number}")
        os.makedirs(question_dir, exist_ok=True)
        markdown_lines = content.get("markdown", [])
        markdown_content = "\n\n".join(markdown_lines)
        for i, img_data in enumerate(content.get("images", [])):
            if isinstance(img_data, str):
                image_filename = f"image_{i + 1}.png"
                image_path = os.path.join(question_dir, image_filename)
                try:
                    with open(image_path, "wb") as img_file:
                        img_file.write(base64.b64decode(img_data))
                    markdown_content += f"\n\n![Image {i + 1}]({image_filename})"
                except Exception as e:
                    print(f"⚠️ Error writing image for question {question_number}, image {i + 1}: {e}")
            else:
                print(f"⚠️ Skipping non-string image data in question {question_number}, image {i + 1}")
        markdown_file_path = os.path.join(question_dir, f"question_{question_number}.md")
        with open(markdown_file_path, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        print(f"✅ Markdown written for Question {question_number} at {markdown_file_path}")







