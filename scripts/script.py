from firebase import FirestoreCRUD
import os

def update_books():
    books_dir = "Data/Books"
    crud = FirestoreCRUD(".firebase_credentials.json")
    books = crud.get_all_books()
    for book in books:
        book_path = os.path.join(books_dir, book.title)
        if not os.path.exists(book_path):
            os.makedirs(book_path)
        for chapter in book.chapters:
            chapter_file = os.path.join(book_path, f"{chapter.chapter_No}_ocr.md")
            with open(chapter_file, 'w', encoding='utf-8') as f:
                f.write(f"Title: {chapter.title}\n\n{chapter.content}")

if __name__ == "__main__":
    update_books()
    print("Books updated successfully.")

