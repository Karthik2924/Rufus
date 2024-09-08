import bs4 as bs
from requests_html import HTMLSession
import requests
import json
import relavance
from relavance import relavance_score   

# class Scraper:
#     def __init__(self, url):
#         self.url = url
#         self.session = HTMLSession()
        
#         try:
#             self.parser = self.session.get(url)
#             self.parser.raise_for_status()  # This will raise an exception for HTTP errors
#             self.soup = bs.BeautifulSoup(self.parser.text, 'lxml')
#         except requests.exceptions.RequestException as e:
#             raise e  # Propagate the error so it can be caught in the tests

#     def get_visible_text(self):
#         text = self.soup.get_text(separator=" ")
#         return text

#     def get_links(self):
#         links = self.parser.html.absolute_links
#         return links


class Scraper:
    def __init__(self, url,handle_exception = True):
        self.url = url
        self.session = HTMLSession()
        self.flag = False
        if handle_exception:
            try:
                self.parser = self.session.get(url)
                self.parser.raise_for_status()  # This will raise an exception for HTTP errors
                self.soup = bs.BeautifulSoup(self.parser.text, 'lxml')
            except requests.exceptions.RequestException as e:
                raise e  # Propagate the error so it can be caught in the tests
        else:
            try:
                self.parser = self.session.get(url)
                self.parser.raise_for_status()  # This will raise an exception for HTTP errors
                self.soup = bs.BeautifulSoup(self.parser.text, 'lxml')
            except:
                self.flag = True
                pass

    def get_visible_text(self):
        if self.flag:
            return "Unique__Placeholder"
        text = self.soup.get_text(separator=" ",strip = True)
        return text

    def get_links(self):
        if self.flag:
            return set()
        links = self.parser.html.absolute_links
        return links
    
     
        
class deep_scrape:
    def __init__(self, url,query = None,relavance_method = 'dpr',depth = 3, max_links = 50,topk = 5):
        '''
        Arguments : 
        url : root url to start exploration from
        query : default None, if provided will use relavance methods for collecting data from links, leave as None to extract every outlink and create a data store
        relavance_method : dpr or bm25, only used if query is not None
        depth : exploration depth starting from root node
        max_links: maximum number of urls to explore, if you donot want this to be a limiting factor, set to very high number but it will take a lot of time
        topk : used if query is present, selects the topk relavant answers.
        
        '''
        self.url = url
        self.session = HTMLSession()
        self.max_depth = depth
        self.max_links = max_links
        self.cur_depth = 0
        self.stack = [url]
        self.vis = set()
        # self.document_store = []
        # self.reference_store = []
        self.data_store = {}
        self.query = query
        self.topk = topk
        self.relavance_method = relavance_method
        if self.query:
            self.relavance = relavance_score(query,relavance_method)
    
    def recursive_scrape(self):
        '''
        Arguments : None
        updates the data store
        
        Tasks:
        Starting from the root url, recursively explores the outlinks
        Terminates when desired depth or explored set links or when no new links are left to explore.
        
        '''
        depth = self.max_depth
        nlinks = self.max_links
        # add text extract from the first element of stack into the document store or context
        while len(self.stack)>0 and depth > 0 and nlinks > 0:
            cur_len = len(self.stack)
            self.vis.union(set(self.stack))
            data,new_urls = self.scrape(self.stack)
            
            # can potentially add an extra pre processing step at the cost of more api calls, to clean the scraped data.
            # can also store vectors if needed
            self.data_store.update(data)
            
            ## self.document_store.extend(new_context)
            ## self.reference_store.extend(reference_urls)
            new_urls = list(new_urls.difference(self.vis))
            self.stack = new_urls

            # update the depth and nlinks value. As this is a terminating condition for this function
            depth -= 1
            nlinks -= cur_len
        
    def scrape(self,urls):
        '''
        Arguments : List of urls to be analyzed
        Returns : Dictionary containing relavant urls as key and text extracted as values, returns next iteration of urls for the next exploration step
        
        Scrapes the urls and provides new urls for the next iteration of recursive search.
        
        If query is present it uses the relevancy measures and picks the top results, 
        otherwise it will just recursively explore the URLs till the desired depth is reached
        or the desired number of urls are analyzed
        
        Potential Improvements : Before adding to the vector store, process the text with text processing
        or using another LLM, but this increases the number of LLM calls and the overall cost.
        
        Todo : Use multiprocessing to parallelize to improve speed.
        '''
        sc_objs = list(map(Scraper,urls,[False]*len(urls)))
        
        sc_urls = list(map(Scraper.get_links,sc_objs))
        # returns a list of sets
        # get a union of all sets in the list
        sc_urls = set().union(*sc_urls)
        
        sc_text = list(map(Scraper.get_visible_text,sc_objs))
        
        if self.query:
            if self.relavance_method == 'dpr':
                scores = self.relavance.dpr_score(sc_text)
            else:
                scores = list(map(self.relavance.bm25_score,sc_text))
                
            topk_texts = sorted(zip(scores,sc_text,urls),key=lambda x : x[0],reverse=True) # higher score means more relavant
            data= {} # dictionary with url : text extracted
            for _,txt,ref in topk_texts[:self.topk]:
                data[ref] = txt
                
            return data, sc_urls
        
        else:
            data = {}
            for i in range(len(urls)):
                data[urls[i]] = sc_text[i]
            
            return data,sc_urls
        
    def save_data_to_file(self, path):
        with open(path,'w') as json_file:
            json.dump(self.data_store,json_file,indent=4)
        