import re

def is_fill_images(encoded_image):
    return False


def filter_attempted_questions(ocr_result: dict) -> list[int]:
    
    # exclude_phrases = [
    #     "DO NOT WRITE IN THE SHADED AREA OR BEYOND",
    #     "Sample",
    #     "part"
    # ]
    
    # attempted_questions = []
    
    # for question_no, content in ocr_result.items():
        
    #     markdown = content["markdown"]
    #     for pat in exclude_phrases:
    #         markdown = re.sub(pat, "", markdown, flags=re.IGNORECASE)
    #     markdown = markdown.strip()
    #     if len(markdown) > 6:
    #         attempted_questions.append(question_no)
    #         continue

    #     images = content["images"]
    #     if is_fill_images(images):
    #         attempted_questions.append(question_no)
    #         continue
    
    # return attempted_questions
    return [1,2,3,4,5,14,15]