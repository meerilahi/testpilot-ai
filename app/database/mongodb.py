# from langchain_community.document_loaders.mongodb import MongodbLoader

# loader = MongodbLoader(
#     connection_string="mongodb+srv://test123:<FcOJ86LA3TynuiDJ>@fastapi-course.sdltkxc.mongodb.net/",
#     db_name="testpilot-ai",
#     collection_name="restaurantsanswersheets",
#     filter_criteria={"borough": "Bronx", "cuisine": "Bakery"},
#     field_names=["name", "address"],
# )

# docs = loader.load()
# len(docs)

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://test123:test123@fastapi-course.sdltkxc.mongodb.net/?retryWrites=true&w=majority&appName=FASTAPI-COURSE"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)