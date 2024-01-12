import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()
import pinecone
from sentence_transformers import SentenceTransformer
import streamlit as st

API_KEY = os.environ.get("API_KEY")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
API_TOKEN = os.environ.get("API_TOKEN")

# Connect to pincecone
pinecone.init(api_key=API_KEY, environment=ENVIRONMENT)
index = pinecone.Index("local-classes-index")

# Loads and caches the model
@st.cache_resource
def load_model():
    return SentenceTransformer("BAAI/bge-base-en-v1.5", use_auth_token=API_TOKEN)

model = load_model()

#
def most_similar():
    user_embedding = model.encode(st.session_state["course_description"]).tolist()
    result = index.query(vector=user_embedding, top_k=3, include_metadata=False)
    top_matches = result["matches"]
    for match in top_matches:
        st.write(f'{match["id"]} is {match["score"] * 100:.2f}% similar')

st.write("# Semantic Search")
with st.form(key="my_form"):
    st.text_input("Enter course description: ", key="course_description")
    st.form_submit_button("Search", on_click=most_similar)