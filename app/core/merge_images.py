from PIL import Image
import base64
from io import BytesIO
from typing import List

def combine_base64_images(image_b64_list: List[str]) -> str:
    images = []

    for img_str in image_b64_list:
        try:
            image_data = base64.b64decode(img_str)
            img = Image.open(BytesIO(image_data)).convert("RGB")
            images.append(img)
        except Exception as e:
            print(f"Failed to decode or open image: {e}")
            continue

    if not images:
        return None
    total_height = sum(img.height for img in images)
    max_width = max(img.width for img in images)

    combined_img = Image.new('RGB', (max_width, total_height), color=(255, 255, 255))
    y_offset = 0
    for img in images:
        combined_img.paste(img, (0, y_offset))
        y_offset += img.height

    buffered = BytesIO()
    combined_img.save(buffered, format="PNG")
    combined_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return combined_b64
