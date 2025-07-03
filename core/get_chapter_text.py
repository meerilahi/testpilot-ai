import os

def get_chapter_text(bookTitle: str, chapter_number: int):
    current_file = os.path.abspath(__file__)
    file_path = os.path.join(os.path.dirname(os.path.dirname(current_file)), 'Data', 'Books', bookTitle, f"{chapter_number}.md")
    print(file_path)
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

