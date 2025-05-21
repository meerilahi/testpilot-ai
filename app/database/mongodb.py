from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.binary import Binary
from langchain_community.document_loaders import PyMuPDFLoader
import re
import fitz
from bson import Binary
from io import BytesIO

uri = "mongodb+srv://test123:test123@fastapi-course.sdltkxc.mongodb.net/?retryWrites=true&w=majority&appName=FASTAPI-COURSE"
client = MongoClient(uri, server_api=ServerApi('1'))

def get_database():
    db = client["testpilot-ai"]
    return db

def get_answer_sheets_collection():
    db = get_database()
    collection = db["answersheets"]
    return collection

def add_answer_sheet(pdf_stream, name):
    answer_sheets_collection = get_answer_sheets_collection()
    binary_data = Binary(pdf_stream.read())
    result = answer_sheets_collection.insert_one({
        "id": name,
        "file_data": binary_data,
        "content_type": "application/pdf"
    })
    return result.inserted_id

def get_answer_sheet(id):
    answer_sheets_colletion = get_answer_sheets_collection()
    doc = answer_sheets_colletion.find_one({"id": id})    
    file_data = doc["file_data"]
    pdf_stream = BytesIO(file_data)
    return pdf_stream

def delete_answer_sheet(id):
    answer_sheets_colletion = get_answer_sheets_collection()
    result = answer_sheets_colletion.delete_one({"id": id})
    return result.deleted_count


def get_books_collection():
    db = get_database()
    collection = db["books"]
    return collection

def add_book(file_path, id):
    books_collection = get_books_collection()
    loader = PyMuPDFLoader(file_path)
    documents = loader.load()   
    for i, doc in enumerate(documents):
        page_id = f"book-{id}-page-{i}"
        books_collection.insert_one({"page_id": page_id, "text": doc.page_content})

def get_book_pages(id, page_numbers):
    books_collection = get_books_collection()
    content = []
    for i in page_numbers:
        page_id = f"book-{id}-page-{i}"
        doc = books_collection.find_one({"page_id": page_id})
        content.append(doc["text"])
    return content

def get_books_ids():
    books_collection = get_books_collection()
    ids_list = books_collection.distinct("page_id")
    book_ids = set()
    for id in ids_list:
        match = re.search(r"book-([^-]+)-page-\d+", id)
        if match:
            book_id = match.group(1)
            book_ids.add(book_id)
    return list(book_ids) 

def delete_book(id):
    books_collection = get_books_collection()
    result = books_collection.delete_many({"page_id": {"$regex": f"^book-{id}-page-"}})
    return result.deleted_count

# with open("app/database/data/sheet.pdf", "rb") as file:
#     pdf_stream = BytesIO(file.read())
# inserted_id = add_answer_sheet(pdf_stream, name="student_123")
# print(f"PDF inserted into MongoDB with ID: {inserted_id}")


# pdf_doc = get_answer_sheet("student_123")
# page = pdf_doc[0]
# pix = page.get_pixmap()
# pix.save("first_page_preview.png")
# print(f"PDF has {len(pdf_doc)} pages.")