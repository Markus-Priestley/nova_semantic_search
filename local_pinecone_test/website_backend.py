import os
from dotenv import load_dotenv
load_dotenv()
import pinecone
from sentence_transformers import SentenceTransformer

API_KEY = os.environ.get("API_KEY")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
API_TOKEN = os.environ.get("API_TOKEN")

pinecone.init(api_key=API_KEY, environment=ENVIRONMENT)
index = pinecone.Index("local-classes-index")

#model = SentenceTransformer("BAAI/bge-base-en-v1.5", use_auth_token=API_TOKEN)

def clear_pinecone():
    delete_response = index.delete(delete_all=True)
    print(delete_response)
    print('cheese')

#user_description = input('Describe the course you are interested in: ')
#user_embedding = model.encode(user_description).tolist()
#result = index.query(vector=user_embedding, top_k=3, include_metadata=False)
#print(result)

clear_pinecone()