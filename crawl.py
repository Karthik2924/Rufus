
import bs4 as bs
from requests_html import HTMLSession
import requests
import urllib.request
from googlesearch import search
import scraper
from scraper import *


class Crawler(scraper.deep_scrape):
    def __init__(self,query,num_queries = 5,relavance_method = 'dpr'):
        self.query = query
        self.num_queries = num_queries
        self.urls = self.get_urls(query,num_queries)
        super().__init__(url = self.urls[0],query = self.query, relavance_method=relavance_method,depth = 1, max_links=num_queries,topk = num_queries)
        self.stack = self.urls

    def get_urls(self,query,num_results = 5):
        return list(search(term = query,num_results=num_results))
    
    def get_data(self):
        self.recursive_scrape()
        context = " "
        for k,v in self.data_store.items():
            context += v + ' '
        return context