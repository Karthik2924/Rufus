
import string
import numpy as np
import requests
import os
from dotenv import load_dotenv, dotenv_values 
import nomic
from nomic import embed
load_dotenv() 


# def get_embedding(text):
      
#     output = embed.text(
#         texts=[text],
#         model='nomic-embed-text-v1.5',
#         task_type='search_document',
#     )
#     return output['embeddings'][0]

# # Function to calculate cosine similarity
# def cosine_similarity(embedding1, embedding2):
#     dot_product = np.dot(embedding1, embedding2)
#     norm1 = np.linalg.norm(embedding1)
#     norm2 = np.linalg.norm(embedding2)
#     return dot_product / (norm1 * norm2)

# # Example pipeline to calculate similarity between query and document
# def calculate_similarity(query, document):
#     query_embedding = get_embedding(query)
#     document_embedding = get_embedding(document)
#     similarity = cosine_similarity(query_embedding, document_embedding)
#     return similarity


class relavance_score:
    def __init__(self,query,method = 'dpr') -> None:
        #method can be bm25 or ('dpr') Dense Passage retrieval with Nomic embeddings    
        self.query = query
        self.method = method
        
        self.stop_words = set(["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", 
                   "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers",
                   "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
                   "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was",
                   "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing",
                   "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", 
                   "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", 
                   "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", 
                   "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", 
                   "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", 
                   "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
                   "will", "just", "don", "should", "now"])
        if self.method == 'bm25':
            self.query_term = self.tokenize(query)
        else:
            load_dotenv() 
            nomic.login(os.environ['NOMIC_API_KEY'])
            self.query_term = np.array(embed.text(
                                    texts=[query],
                                    model='nomic-embed-text-v1.5',
                                    task_type='search_query',
                                )['embeddings'])
            self.query_term = self.query_term  / np.linalg.norm(self.query_term, axis=1, keepdims=True)

        
    def tokenize(self,text):
        # Remove punctuation and convert to lowercase
        text = text.translate(str.maketrans('', '', string.punctuation)).lower()
        # Split into words and remove stop words
        return [word for word in text.split() if word not in self.stop_words]
    def bm25_score(self, document, k1=1.5, b=0.75,idf = 1.0):
        # call this function with map,list(documents) to match the output with that of dpr_score
        # can be parallelized and is light weight, but very naive

        doc_terms = self.tokenize(document)
        dl = len(doc_terms)
        avgdl = dl
        N = 1

        tf = {term: doc_terms.count(term) for term in set(self.query_term)}
        
        score = 0.0
        for term in self.query_term:
            if term in tf:
                freq = tf[term]
                score_term = (idf * (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * (dl / avgdl))))
                score += score_term
        return score
    
    
    def dpr_score(self,documents):
        #dense passage retrieval with Nomic Embeddings
        document_embeddings = embed.text(
                    texts=documents,
                    model='nomic-embed-text-v1.5',
                    task_type='search_document',
                )['embeddings']
        document_embeddings = np.array(document_embeddings)
        
        # Normalization Step for document embeddings, queries already normalized
        document_embeddings =  document_embeddings / np.linalg.norm(document_embeddings, axis=1, keepdims=True)
        
        # Computer Cosine similarity and flattent the data
        cosine_sim = np.dot(document_embeddings, self.query_term.T) 
        cosine_sim_flat = cosine_sim.flatten()
        
        #convert to list before returning to keep the api similar to bm25_score
        return list(cosine_sim_flat)
    
    
        
