from typing import List
import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from scripts.book_model import BookModel, ChapterModel

class FirestoreCRUD:

    def __init__(self, cred_path: str = None):
        if not firebase_admin._apps:
            if cred_path:
                cred = credentials.Certificate(cred_path)
            else:
                cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        self.books_collection = "books"

    def add_book(self, book: BookModel) -> str:
        doc_ref = self.db.collection(self.books_collection).document()
        doc_ref.set(book.to_dict())
        return doc_ref.id
    
    def add_chapter_to_book(self, book_id: str, chapter: ChapterModel) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()    
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        book.chapters.append(chapter)
        book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
        return True

    def get_book(self, book_id: str) -> BookModel:
        doc_ref = self.db.collection(self.books_collection).document(book_id)
        doc = doc_ref.get()
        if doc.exists:
            return BookModel.from_dict(doc.to_dict())
        return None

    def get_all_books(self) -> List[BookModel]:
        docs = self.db.collection(self.books_collection).stream()
        return [BookModel.from_dict(doc.to_dict()) for doc in docs]

    def get_books_by_title(self, title: str) -> List[BookModel]:
        docs = self.db.collection(self.books_collection)\
                      .where(filter=FieldFilter('title', '>=', title))\
                      .where(filter=FieldFilter('title', '<=', title + '\uf8ff'))\
                      .stream()
        return [BookModel.from_dict(doc.to_dict()) for doc in docs]

    def get_chapter(self, book_id: str, chapter_no: int) -> ChapterModel:
        book = self.get_book(book_id)
        if book and book.chapters:
            for chapter in book.chapters:
                if chapter.chapter_No == chapter_no:
                    return chapter
        return None

    def update_book_title(self, book_id: str, new_title: str) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_ref.update({'title': new_title})
        return True

    def update_chapter(self, book_id: str, chapter_no: int, new_chapter: ChapterModel) -> bool:
        if new_chapter.chapter_No != chapter_no:
            return False
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        updated = False
        for i, chapter in enumerate(book.chapters):
            if chapter.chapter_No == chapter_no:
                book.chapters[i] = new_chapter
                updated = True
                break
        if updated:
            book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
            return True
        return False

    def delete_book(self, book_id: str) -> bool:
        self.db.collection(self.books_collection).document(book_id).delete()
        return True

    def delete_chapter(self, book_id: str, chapter_no: int) -> bool:
        book_ref = self.db.collection(self.books_collection).document(book_id)
        book_data = book_ref.get().to_dict()
        if not book_data:
            return False
        book = BookModel.from_dict(book_data)
        original_length = len(book.chapters)
        book.chapters = [ch for ch in book.chapters if ch.chapter_No != chapter_no]
        if len(book.chapters) < original_length:
            book_ref.update({'chapters': [ch.to_dict() for ch in book.chapters]})
            return True
        return False


