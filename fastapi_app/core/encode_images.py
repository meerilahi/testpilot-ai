import base64
from io import BytesIO
from PIL import Image

def encode_images_to_base64(image_dict, format='JPEG'):
    encoded_dict = {}
    for key, img_list in image_dict.items():
        encoded_list = []
        for img in img_list:
            buffered = BytesIO()
            img.save(buffered, format=format)
            encoded_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            encoded_list.append(encoded_str)
        encoded_dict[key] = encoded_list

    return encoded_dict
