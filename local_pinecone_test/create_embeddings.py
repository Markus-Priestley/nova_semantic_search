import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from sentence_transformers import SentenceTransformer

API_TOKEN = os.environ.get("API_TOKEN")

# Load in the model
model = SentenceTransformer("BAAI/bge-base-en-v1.5", use_auth_token=API_TOKEN)

# Convert csv into pandas dataframe
relative_csv_path = "local_test_supabase/course_info.csv"
class_csv = os.path.abspath(relative_csv_path)
df = pd.read_csv(class_csv)

# Applies get_embeddings function to all rows in the descriptions column and adds the result to the dataframe as the embeddings column
description_column = "PDF"
embeddings_column = "description_embeddings"
df[embeddings_column] = df[description_column].apply(lambda x: model.encode(str(x)))
print(df.head())

# Converts dataframe back into csv with new embeddings column
relative_new_csv_path = "local_test_supabase/embeddings.csv"
embeddings_csv = os.path.abspath(relative_new_csv_path)
df.to_csv(embeddings_csv)