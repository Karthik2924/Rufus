import scraper,crawl
from scraper import *
from crawl import *
import json
import cohere
from dotenv import load_dotenv, dotenv_values 
load_dotenv()
import os

class Rufus(Crawler,Scraper):
    def __init__(self,model = 'command-r'):
        '''
        This class is an interface for different methods to scrape the web.
        Todo : add api client code here
        '''
        # Add cohere generation here
        load_dotenv()
        self.co = cohere.Client(api_key=os.environ['COHERE_API_KEY'])
        
        self.model = model
        # response = self.co.chat(
        #         model=self.model,
        #         message = "What is machine Learning"
        #         )
        
        #Can do Api authentication for Rufus aswell, Currently this part doesn't work
        # TO DO
        self.id = 'xyz'
    
    def scrape_url(self,url, handle_exception = True):
        self.scraper = Scraper(url,handle_exception)
        context_from_url = self.scraper.get_visible_text()
        res = self.clean_crawled_data(context_from_url)
        return {"cleaned_data": res , "raw_data": context_from_url}
    
    def deep_scrape_url(self,url,query = None,relavance_method = 'dpr', max_links = 10, topk = 5, depth = 3):
        self.deep_scraper = deep_scrape(url = url,query = query,
                                        relavance_method = relavance_method,depth = depth,
                                        max_links = max_links,topk = topk)
        self.deep_scraper.recursive_scrape()
        context = " "
        for k,v in self.deep_scraper.data_store.items():
            context += v + ' '
        return self.generate_answer(query,context,True,False)
        #return context
    
    def crawl_web(self,query,num_queries = 5):
        self.crawler = Crawler(query,num_queries=num_queries)
        context = self.crawler.get_data()
        return self.generate_answer(query,context,True,False)
        
    def clean_crawled_data(self,text):
        response = self.co.chat(
                    model=self.model,
                    message = text + '''Above is the text obtained from web scraping. 
                    Clean the above data so that it can be viewed by humans or could act as context for a Large language model.'''
                    )
        return response.text
    
    def generate_answer(self,query,context,print_ = True,clean_data=False):
        response = self.co.chat(
            model=self.model,
            message = context + '''Above is the context obtained by scraping multiple webpages, process it appropriately and answer the query. Query = ''' + query
            )
        if print_:
            print(response.text)
        return response.text
        