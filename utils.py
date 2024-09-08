import numpy as np
import requests
import os
from dotenv import load_dotenv, dotenv_values 
import nomic
from nomic import embed
load_dotenv() 


nomic.login(os.environ['NOMIC_API_KEY'])

def get_embedding(text):
      
    output = embed.text(
        texts=[text],
        model='nomic-embed-text-v1.5',
        task_type='search_document',
    )
    return output['embeddings'][0]

# Function to calculate cosine similarity
def cosine_similarity(embedding1, embedding2):
    dot_product = np.dot(embedding1, embedding2)
    norm1 = np.linalg.norm(embedding1)
    norm2 = np.linalg.norm(embedding2)
    return dot_product / (norm1 * norm2)

# Example pipeline to calculate similarity between query and document
def calculate_similarity(query, document):
    query_embedding = get_embedding(query)
    document_embedding = get_embedding(document)
    similarity = cosine_similarity(query_embedding, document_embedding)
    return similarity

# # Sample query and document
# query = "What is artificial intelligence?"
# document = "Artificial intelligence refers to the simulation of human intelligence in machines that are programmed to think and learn."

# # Calculate similarity
# similarity_score = calculate_similarity(query, document)
# print(f"Similarity between query and document: {similarity_score}")

