import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import logging
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from .utils import normalize_url, is_valid_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_links_and_text(base_url, url, pdf_path):
    """
    Scrape all valid links and the body text from a given URL, and save the text as a PDF.

    Args:
        base_url (str): The base URL for link normalization.
        url (str): The target URL to scrape.
        pdf_path (str): The directory path to save the PDF file.

    Returns:
        list: A list of valid, normalized links.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, 'lxml')
    except Exception as e:
        logger.error(f"Failed to parse HTML: {e}")
        return []

    try:
        links = [
            normalize_url(url, a['href']) 
            for a in soup.find_all('a', href=True) 
            if is_valid_url(normalize_url(url, a['href']), base_url)
        ]
    except Exception as e:
        logger.error(f"Error processing links: {e}")
        return []

    body_text = soup.get_text()

    try:
        save_text_as_pdf(body_text, pdf_path, url)
    except Exception as e:
        logger.error(f"Failed to save PDF: {e}")
        return []

    return links

def save_text_as_pdf(text, path, url):
    """
    Create a PDF file from the provided text, using text wrapping, named after the page's URL components.

    Args:
        text (str): The text content to save in the PDF.
        path (str): The directory path to save the PDF file.
        url (str): The URL of the page being saved.

    Returns:
        None
    """
    try:
        file_name = urlparse(url).path.strip('/').replace('/', '_') or "index"
        file_path = os.path.join(path, f"{file_name}.pdf")

        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        text = text.encode('utf-8', 'replace').decode('utf-8')
        story.append(Paragraph(text, styles['BodyText']))

        doc.build(story)
    except Exception as e:
        logger.error(f"Error creating PDF: {e}")