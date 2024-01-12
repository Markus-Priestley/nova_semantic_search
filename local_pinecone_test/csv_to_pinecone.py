import os
from dotenv import load_dotenv
load_dotenv()
import pinecone
import pandas as pd
import ast
import random
import time

# Connect to pinecone
API_KEY = os.environ.get("API_KEY")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
pinecone.init(api_key=API_KEY, environment=ENVIRONMENT)
index = pinecone.Index("local-classes-index")

# Load in the CSV as a dataframe
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_file_name = 'clean_embeddings.csv'
csv_path = f"{current_directory}/{csv_file_name}"
df = pd.read_csv(csv_path, index_col='Class')

# Creates dataframe with classes whos name were not extracted by the regular expressions
filtered_df = df[df['class_name'].isnull()]
# Manually enters these class names into a dictionary
shit_data = {'DNA 130': 'DNA 1 30 DENTAL OFFICE MANAGEMENT', 'DNA 134': 'DNA 1 34 DENTAL RADIOLOGY AND PRACTICUM I', 'ESL 24': 'ESL 24 ORAL AND WRITTEN COMMUNICATIONS I',
             'HRI 251': 'HRI 251 FOOD AND BEVERAGE COST CONTROL I', 'HRI 265': 'HRI 265 HOTEL FRONT OFFICE OPERATIONS', 'ITN 120': 'ITN 120 WIRELESS NETWORK ADMINISTRATION W NA',
             'ITP 136': 'ITP 136 C PROGRAMMING I', 'ITP 270': 'ITP 270 PROGRAMMING FOR CYBERSECURITY', 'LBR 105': 'LBR 105 LIBRARY SKILLS FOR RESEARCH', 'MTE 8': 'MTE 8 RATIONAL EXPONENTS AND RADICALS',
             'OCT 190': 'OCT 190 COORDINATED INTERNSHIP', 'OCT 290': 'OCT 290 COORDINATED INTERNSHIP LEVEL II FIELDWORK', 'PED 166': 'P E D 166 BALLET I', 'SDV 107': 'SDV 107 CAREER EDUCATION',
             'SSC 205': 'SSC 205 CULTURAL AND SOCIAL STUDY OF WOMEN', 'TRV 290': 'TRV 290 COORDINATED INTERNSHIP'}
# Filter out the classes for which class_name was not extracted
df = df[~df.index.isin(shit_data)]

# List will hold all tuples that will be upserted into the pinecone vector db
upsert_list = []
# Iterates through rows of the dataframes and formats the tuples that are added to upsert_list
for row in df.itertuples():
    # Converts the embedding from a string into a list
    embedding = ast.literal_eval(row.description_embeddings)
    # Formats and adds tuples into upsert_list
    upsert_list.append((row.class_name, embedding, {"Department": row.Department, "Description": row.PDF}))
# Does the same as the above for loop but for the rows where class_name had to be manually enterede
for row in filtered_df.itertuples():
    embedding = ast.literal_eval(row.description_embeddings)
    upsert_list.append((shit_data[row.Index], embedding, {"Department": row.Department, "Description": row.PDF}))

# Seperates upsert list into chunks of at most 100
lower_cut = 0
upper_cut = 100
# If this condition is true, there are tupels in upsert_list that have yet to be upserted into pinecone
while lower_cut <= len(upsert_list):
    # Upserts chunck of upser_list and prints upsert response
    upsert_response = index.upsert(upsert_list[lower_cut:upper_cut])
    print(upsert_response)
    # Sets cuts to the index of next 100 tuples to be upserted
    lower_cut += 100
    upper_cut += 100
    # Sleeps a random time to prevent flooding pinecone with requests
    sleep_time = random.randrange(5, 10)
    time.sleep(sleep_time)