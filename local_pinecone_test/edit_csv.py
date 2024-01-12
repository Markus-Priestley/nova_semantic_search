import os
import pandas as pd

# Function removes the index column added when a CSV is converted into a dataframe. Unecessary
# if you set the index column of the dataframe to one of the columns in the CSV
def remove_index_column(file_name, new_file_name):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_name = file_name
    embeddings_csv_path = f"{current_directory}/{csv_file_name}"
    df = pd.read_csv(embeddings_csv_path)
    #df = df[df['Department'] == 'ACC']
    column_index_to_delete = 0
    df = df.drop(df.columns[column_index_to_delete], axis=1)
    new_embeddings_csv = new_file_name
    new_csv_path = f"{current_directory}/{new_embeddings_csv}"
    df.to_csv(new_csv_path, index=False, mode='w')

# Function attempts to clean the PDF column of the CSV. Input file_name for new_file_name if you would
    # Like to rewrite the file. To create a new file input a unique file name for new_file_name
def clean_csv(file_name, new_file_name):
    # Load in the csv
    current_directory = os.path.dirname(os.path.abspath(__file__))
    csv_file_name = file_name
    embeddings_csv_path = f"{current_directory}/{csv_file_name}"
    df = pd.read_csv(embeddings_csv_path)
    # Fills empty entries in the dataframe with none
    df = df.fillna('None')
    # Excludes the classes without a PDF from the dataframe
    df = df[df['PDF'] != 'None']
    # Regular expressions remove new line charachters, excess spaces, and unconventional characters.
    df['PDF'] = df['PDF'].str.replace('[^a-zA-Z0-9\s.,;:]', '', regex=True)
    df['PDF'] = df['PDF'].str.replace('\n', '')
    df['PDF'] = df['PDF'].str.strip()
    df['PDF'] = df['PDF'].str.replace(r'[^\S ]', ' ', regex=True)
    df['PDF'] = df['PDF'].str.replace(' +', ' ', regex=True)
    # Extracts class name from PDF column into a new column called class_name
    start = 'S\s?U\s?M\s?M\s?A\s?R\s?Y'
    stop = '\s?C\s?R\s?[\.\s]'
    pattern = rf'{start}\s+(.*?)(?=\d{stop})'
    df['class_name'] = df['PDF'].str.extract(pattern)
    # Convert dataframe bade into a csv
    new_csv = new_file_name
    new_csv_path = f"{current_directory}/{new_csv}"
    df.to_csv(new_csv_path, index=False, mode='w')

clean_csv("embeddings.csv", 'clean_embeddings.csv')