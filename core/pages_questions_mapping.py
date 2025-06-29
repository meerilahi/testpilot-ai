from PIL import Image
from typing import List, Dict

PAGES_QUESTIONS_MAPPING: Dict[int, List[int]] = {
    1: [4],
    2: [5],
    3: [6],
    4: [7],
    5: [8],
    6: [9],
    7: [10],
    8: [11],
    9: [12],
    10: [13],
    11: [14],
    12: [15,16,17,18],
    13: [19,20,21,22],
    14: [23,24,25,26],
    15: [27,28,29,30],    
}

def map_pages_to_questions(images: Image.Image) -> Dict[int, List[Image.Image]]:
    dictionary_mapping = {}
    for key, values in PAGES_QUESTIONS_MAPPING.items():
        dictionary_mapping[key] = [images[i-1] for i in values if i-1 < len(images)]
    return dictionary_mapping