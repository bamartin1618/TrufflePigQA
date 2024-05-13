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

def scrape_links_and_text(base_url, url, pdf_path):
    """
    Scrape links and text from a given URL and save content to a PDF.

    Args:
        base_url (str): The base URL to resolve relative links.
        url (str): The URL to scrape.
        pdf_path (str): The path to save the PDF content.

    Returns:
        list: A list of extracted links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except RequestException as e:
        logging.error(f"Failed to retrieve {url}: {e}")
        return []
    
    # Placeholder for parsing logic
    links = []
    try:
        # Assume some parsing logic here
        # links = parse_links(response.content, base_url)
        pass
    except Exception as e:
        logging.error(f"Failed to parse content from {url}: {e}")
        return []

    # Saving response content to a PDF file
    try:
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(response.content)
    except IOError as e:
        logging.error(f"Failed to write to {pdf_path}: {e}")
        return []

    return links