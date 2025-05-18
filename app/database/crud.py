from uuid import uuid4
from typing import List
from langchain.docstore.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from pinecone_db import get_index
from typing import List
import re

load_dotenv()

index = get_index()
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
    print(f"✅ Book uploaded to namespace: {namespace} with book_id: {book_id}")
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
    ids_generator = index.list(namespace=namespace)
    
    book_ids = set()
    pattern = re.compile(r"book-([a-f0-9]+)-page-\d+")

    for item in ids_generator:
        # If item is a string, use it as-is
        # If it's a dict or object, try to get the 'id' field
        if isinstance(item, str):
            vid = item
        elif isinstance(item, dict) and 'id' in item:
            vid = item['id']
        else:
            continue  # skip anything unexpected

        match = pattern.match(vid)
        if match:
            book_ids.add(match.group(1))

    return list(book_ids)


book_ids = get_books_ids()
print("✅ Book IDs found:", book_ids)

# loader = PyPDFLoader("book.pdf")
# pages = loader.load()
# book_id = add_new_book(pages)


# book_id = "698daf88c3a84ce6b282fc24f59a1653"
# pages_to_fetch = [0, 1, 5]
# contents = get_book_pages(book_id, pages_to_fetch)
# for i, content in zip(pages_to_fetch, contents):
#     print(f"\n📄 Page {i} Content:\n{content}")


