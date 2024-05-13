import requests
from requests.exceptions import RequestException
import logging
import os

from .scraper import scrape_links_and_text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def crawl(url, base_url, visited_urls, pdf_path):
    """
    Recursively crawl starting from a given URL.

    Args:
        url (str): The URL to crawl.
        base_url (str): The base URL to resolve relative links.
        visited_urls (set): A set of already visited URLs to avoid revisits.
        pdf_path (str): The path to save the PDF content.
    """
    if url in visited_urls:
        logging.info(f"Already visited: {url}")
        return
    visited_urls.add(url)
    logging.info(f"Crawling: {url}")

    try:
        links = scrape_links_and_text(base_url, url, pdf_path)
    except RequestException as e:
        logging.error(f"Network error while trying to scrape {url}: {e}")
        return
    except Exception as e:
        logging.error(f"An error occurred while scraping {url}: {e}")
        return

    for link in links:
        crawl(link, base_url, visited_urls, pdf_path)
