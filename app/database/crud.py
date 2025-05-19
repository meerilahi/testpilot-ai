from uuid import uuid4
from typing import List
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from pinecone_db import get_pinecone_index
from typing import List
import re

load_dotenv()

index = get_pinecone_index()
embedding_model = HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-large")

def add_new_book(pages: List[Document]):
    namespace = "books"
    book_id = uuid4().hex
    vectors = []
    for i, page in enumerate(pages):
        page_id = f"book-{book_id}-page-{i}"
        vector = embedding_model.embed_query(page.page_content)
        vectors.append({
            "id": page_id,
            "values": vector,
            "metadata": {
                "page_number": i,
                "content": page.page_content
            }
        })
    index.upsert(vectors=vectors, namespace=namespace)
    return page_id


def get_book_pages(book_id: str, page_numbers: List[int]) -> List[str]:
    namespace = "books"
    ids = [f"book-{book_id}-page-{i}" for i in page_numbers]
    response = index.fetch(ids=ids, namespace=namespace)
    contents = []
    for page_id in ids:
        item = response.vectors.get(page_id)
        contents.append(item.metadata['content'])
    return contents


def get_books_ids() -> List[str]:
    namespace = "books"
    ids_list = list(index.list(namespace=namespace))[0]
    book_ids = set()
    for id in ids_list:
        match = re.search(r"book-([^-]+)-page-\d+", id)
        if match:
            book_id = match.group(1)
            book_ids.add(book_id)
    return list(book_ids)

# from langchain_community.document_loaders import PyPDFLoader
# loader = PyPDFLoader("book.pdf")
# pages = loader.load()
# book_id = add_new_book(pages)

# book_id = "698daf88c3a84ce6b282fc24f59a1653"
# pages_to_fetch = [0, 1, 5]
# contents = get_book_pages(book_id, pages_to_fetch)

# book_ids = get_books_ids()







