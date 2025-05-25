from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_community.document_loaders import PyMuPDFLoader
import re
from io import BytesIO
from gridfs import GridFS


uri = "mongodb+srv://test123:test123@fastapi-course.sdltkxc.mongodb.net/?retryWrites=true&w=majority&appName=FASTAPI-COURSE"
client = MongoClient(uri, server_api=ServerApi('1'))

def get_db():
    db = client["testpilot-ai"]
    return db

def get_answer_sheets_collection():
    db = get_db()
    collection = db["answersheets"]
    return collection

def add_answer_sheet(pdf_stream, name):
    db = get_db()
    fs = GridFS(db)
    existing = fs.find_one({"filename": name})
    if existing:
        fs.delete(existing._id)
    file_id = fs.put(pdf_stream.read(), filename=name, content_type="application/pdf")
    return file_id


def get_answer_sheet(name):
    db = get_db()
    fs = GridFS(db)

    file = fs.find_one({"filename": name})
    if not file:
        return None

    return BytesIO(file.read())

def delete_answer_sheet(id):
    answer_sheets_colletion = get_answer_sheets_collection()
    result = answer_sheets_colletion.delete_one({"id": id})
    return result.deleted_count


def get_books_collection():
    db = get_db()
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


# with open("temp_data/answer_sheet2.pdf", "rb") as file:
#     pdf_stream = BytesIO(file.read())
# inserted_id = add_answer_sheet(pdf_stream, name="biology2")
# print(f"PDF inserted into MongoDB with ID: {inserted_id}")

# pdf_stream = get_answer_sheet("biology")
# with open("answer_sheet2.pdf", "wb") as f:
#     f.write(pdf_stream.read())