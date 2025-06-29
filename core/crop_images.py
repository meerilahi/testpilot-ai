from PIL import Image
from typing import List, Dict

def crop_images(images : List[Image.Image], left, top, right, bottom):
    cropped_images = []
    for img in images:
        width, height = img.size
        cropped_img = img.crop((
            left,
            top,
            width - right,
            height - bottom
        ))
        cropped_images.append(cropped_img)
        
    return cropped_images
