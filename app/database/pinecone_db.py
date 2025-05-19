import os
from dotenv import load_dotenv
from pinecone import Pinecone
# from pinecone.grpc import PineconeGRPC as Pinecone
load_dotenv()

def get_pinecone_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(host="https://testpilot-ai-yal8jbu.svc.aped-4627-b74a.pinecone.io")
    return index