from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.binary import Binary
from langchain.document_loaders import PyMuPDFLoader
import re

uri = "mongodb+srv://test123:test123@fastapi-course.sdltkxc.mongodb.net/?retryWrites=true&w=majority&appName=FASTAPI-COURSE"
client = MongoClient(uri, server_api=ServerApi('1'))

def get_database():
    db = client["testpilot-ai"]
    return db

def get_answer_sheets_collection():
    db = get_database()
    collection = db["answersheets"]
    return collection

def add_answer_sheet(file_path, name):
    answer_sheets_colletion = get_answer_sheets_collection()
    with open(file_path, "rb") as f:
        binary_data = Binary(f.read())
        result = answer_sheets_colletion.insert_one({
            "id": name,
            "file_data": binary_data,
            "content_type": "application/pdf"
        })
    return result.inserted_id

def get_answer_sheet(id, output_path):
    answer_sheets_colletion = get_answer_sheets_collection()
    doc = answer_sheets_colletion.find_one({"id": id})    
    with open(output_path, "wb") as f:
        f.write(doc["file_data"])

def delete_answer_sheet(id):
    answer_sheets_colletion = get_answer_sheets_collection()
    result = answer_sheets_colletion.delete_one({"id": id})
    return result.deleted_count

# add_answer_sheet("app/database/data/test.pdf", "test")
# get_answer_sheet("test", "app/database/data/test2.pdf")
# delete_answer_sheet("test")


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


# add_book("app/database/data/test2.pdf", "test2")
# print(get_book_pages("test2", [0, 1, 2]))
# print(get_books_ids())
# delete_book("test2")