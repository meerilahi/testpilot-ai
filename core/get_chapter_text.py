import os

def get_chapter_text(bookTitle: str, chapter_number: int):
    current_file = os.path.abspath(__file__)
    file_path = os.path.join(os.path.dirname(current_file),  'Data', bookTitle,  f"{chapter_number}.md")
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

