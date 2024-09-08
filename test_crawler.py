import pytest
from scraper import Scraper
# Test a valid URL
def test_get_visible_text_valid_url():
    url = "https://www.sf.gov"
    scraper = Scraper(url)
    text = scraper.get_visible_text()
    
    assert isinstance(text, str), "Visible text should be a string"
    assert len(text) > 0, "The page should have some visible text"

def test_get_links_valid_url():
    url = "https://www.sf.gov"
    scraper = Scraper(url)
    links = scraper.get_links()
    
    assert isinstance(links, set), "Links should be returned as a set"
    assert len(links) > 0, "The page should have some links"

def test_invalid_url():
    url = "https://invalid-url.com"
    with pytest.raises(requests.exceptions.RequestException):
        scraper = Scraper(url)
        scraper.get_visible_text()


test_get_visible_text_valid_url()
test_get_links_valid_url()
test_invalid_url()