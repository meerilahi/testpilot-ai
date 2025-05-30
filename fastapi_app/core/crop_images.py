from PIL import Image
from typing import List, Dict

def crop_images_in_dict(image_dict : Dict[int,List[Image.Image]], left, top, right, bottom):
    cropped_dict = {}
    for key, img_list in image_dict.items():
        cropped_list = []
        for img in img_list:
            width, height = img.size
            cropped_img = img.crop((
                left,
                top,
                width - right,
                height - bottom
            ))
            cropped_list.append(cropped_img)
        cropped_dict[key] = cropped_list

    return cropped_dict
