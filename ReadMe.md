# Rufus : AI Agent for Web Scrawling

## Main Features : 
* Can recursively scrape selected web pages
* Scrawl with web and scrape web pages based on necessity to answer queries.
* Processes and stores data : Can be used for RAG pipelines later on.

## Setup : 
* Tested with Python3.9
* Download the required libraries from requirements.txt
* create a .env file in the same directory and add API keys for Cohere and Nomic
* Will update the repository to make the instructions more clear, meanwhile if you have an questions. Feel free to open a pull request or reach out to me.

## Documentation : 
* Rufus.py acts as a wrapper for Crawler, Scraper and deep_scrape methods.
* Refer to rufus.ipynb for a brief example on how to use some of the methods.
* For downloading the data to a json file from deep scraper to be used for RAG, you can use the deep_scrape.save_data_to_file method. Provide a path name as input.

## Near Future Updates
* Add more scrapers to scrape more difficult dynamic websites and pdfs and other types of urls.
* Option for parallel processing with multiprocess.
* Add a streaming optioin to Rufus.
* Improve documentation and examples.
  
