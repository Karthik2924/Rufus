# Rufus: AI-Powered Web Scraping and Data Retrieval Agent

Rufus is an intelligent web scraping and data retrieval agent that combines web crawling, scraping, and AI-powered text generation to provide comprehensive answers to user queries.

## Features

- **Web Scraping**: Extracts visible text and links from web pages.
- **Deep Web Crawling**: Recursively explores web pages to a specified depth.
- **Google Search Integration**: Uses Google search to find relevant web pages.
- **AI-Powered Answer Generation**: Utilizes Cohere's language models to generate human-like responses.
- **Relevance Scoring**: Implements both Dense Passage Retrieval (DPR) and BM25 for content relevance ranking.

## Components

1. **Rufus**: The main class that integrates all functionalities.
2. **Crawler**: Handles web crawling using Google search.
3. **Scraper**: Manages web scraping of individual pages and deep crawling.
4. **Relevance**: Implements relevance scoring methods.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from rufus import Rufus

# Initialize Rufus
rufus = Rufus()

# Scrape a single URL
result = rufus.scrape_url("https://example.com")

# Crawl the web for a query
answer = rufus.crawl_web("What is machine learning?")

# Deep scrape a URL
answer = rufus.deep_scrape_url("https://example.com", query="How does this website work?")
```

### Advanced Usage

```python
# Deep scrape without a query (for data collection)
rufus.deep_scrape_url("https://example.com", depth=5, max_links=100)

# Access scraped data
data = rufus.deep_scraper.data_store

# Save scraped data to a file
rufus.deep_scraper.save_data_to_file("scraped_data.json")
```

## Configuration

- Set up environment variables:
  - `COHERE_API_KEY`: Your Cohere API key for text generation.
  - `NOMIC_API_KEY`: Your Nomic API key for embeddings (if using DPR).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

None. Will be updated Soon.

## Disclaimer

This tool is for educational and research purposes only. Always respect websites' terms of service and robots.txt files when scraping.
