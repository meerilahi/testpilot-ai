from mistralai import Mistral
import os
from pathlib import Path
from dotenv import load_dotenv
from mistralai import DocumentURLChunk

load_dotenv() 

client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    
def pdf_to_markdown(pdf_stream) -> str:
  
  uploaded_file = client.files.upload(
      file={
          "file_name": "temp",
          "content": pdf_stream.getvalue(),
      },
      purpose="ocr",
  )
  signed_url = client.files.get_signed_url(file_id=uploaded_file.id, expiry=1)
  pdf_response = client.ocr.process(document=DocumentURLChunk(document_url=signed_url.url),
                                    model="mistral-ocr-latest",
                                    include_image_base64=True)
  markdowns: list[str] = []
  for page in pdf_response.pages:
    markdowns.append(page.markdown)
  return "\n\n".join(markdowns)

# sheet = get_answer_sheet("student_123")
# markdown = pdf_to_markdown(sheet)
# print(markdown)
# with open("output.md", "w", encoding="utf-8") as f:
#     f.write(markdown)


    

