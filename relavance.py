
import string
import numpy as np
import requests
import os
from dotenv import load_dotenv, dotenv_values 
import nomic
from nomic import embed
load_dotenv() 


class relavance_score:
    def __init__(self,query,method = 'dpr') -> None:
        '''
        Arguments : 
        query : (string) Natural language prompt
        method : Technique to measure relavance, 
                currently supports'dense passage retrieval' with Nomic embeddings and bm25 with a single document
                
        Todo : Add support to other embedding models, or provide a wrapper to use custom embedding model of use's choice.
        '''
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
        
        # based on the method, process the query. 
        # Query needs to be processed only once so processing it here and storing it will be benificial in terms of performance
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
        '''
        Arguments : 
        document : string against which query relavance is measured.
        k1 = set to default
        b = 0.75 set to default
        idf : set to 1 (donot change) since working at a document level and not corpus level
                can move this to the code
        
        Returns : Retrieval score to the query, higher is better
        
        Notes
        * * * call this function with map,list(documents) to match the output with that of dpr_score
        * can be parallelized and is light weight
        * method is light weight but very naive compared to state of the art, works at word level
        
        Todo : 
        Ensure the main api is giving option to set the hyperparameters k1, b and move idf down to the code.
        
        '''
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
        '''
        Arguments : 
        Documents : string against which query relavance is measured.
        
        Returns : Cosine similarity, higher is better 
        
        
        Notes
        #dense passage retrieval with Nomic Embeddings

        '''
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
    
    
        
