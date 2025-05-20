from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from PIL import Image
from io import BytesIO
from app.utils.pdf_to_images import pdf_to_images
from app.utils.image_to_data_url import image_to_data_url
import base64


chat = ChatOpenAI(model="gpt-4-vision-preview", max_tokens=2048)

def extract_md_from_image(image: Image.Image) -> str:
    prompt = [
        HumanMessage(
            content=[
                {"type": "text", "text": (
                    "This is a scanned page of a student's handwritten answer sheet. "
                    "Please extract the text exactly as it is and convert it into structured Markdown format. "
                    "Preserve the original formatting: headings, numbered answers, spellings, bullet points, and spacing. "
                    "Avoid summarizing. Output only valid Markdown."
                )},
                {"type": "image_url", "image_url": {"url": image_to_data_url(image)}}
            ]
        )
    ]
    return chat.invoke(prompt).content



def extract_markdown_from_pdf(sheet):
    images = pdf_to_images(sheet)
    markdown_pages = []
    for i, img in enumerate(images):
        markdown = extract_md_from_image(img)
        markdown_pages.append(f"<!-- Page {i+1} -->\n\n{markdown}")
    return "\n\n".join(markdown_pages)

# markdown_output = extract_markdown_from_pdf("scanned_answersheet.pdf")
