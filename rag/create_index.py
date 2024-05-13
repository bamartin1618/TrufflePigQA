import os
import logging
from webscraper.crawler import crawl
from webscraper.utils import normalize_url
from trufflepig import Trufflepig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
BASE_URL = os.getenv('BASE_URL', 'https://trufflepig.mintlify.app/')
PDF_PATH = os.getenv('PDF_PATH', 'rag/pdfs/')
TRUFFLE_KEY = os.getenv('TRUFFLE_KEY')

if not TRUFFLE_KEY:
    raise ValueError("TRUFFLE_KEY environment variable not set")

def ensure_directory_exists(path):
    """Ensure the directory exists."""
    try:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Directory '{path}' is ready.")
    except Exception as e:
        logging.error(f"Error creating directory '{path}': {e}")
        raise

def main():
    """Main function to execute the web scraping and document uploading."""
    ensure_directory_exists(PDF_PATH)

    visited_urls = set()
    try:
        crawl(normalize_url(BASE_URL, ''), BASE_URL, visited_urls, PDF_PATH)
        logging.info("Crawling completed successfully.")
    except Exception as e:
        logging.error(f"Error during crawling: {e}")
        return

    try:
        file_paths = [os.path.join(PDF_PATH, file_path) for file_path in os.listdir(PDF_PATH)]
        files = [{'document_path': path} for path in file_paths]
    except Exception as e:
        logging.error(f"Error listing files in '{PDF_PATH}': {e}")
        return

    try:
        client = Trufflepig(TRUFFLE_KEY)
        index = client.create_index('truffle-pig-qa')
        document_keys = index.upload(files=files)
        upload_status = index.get_upload_status(document_keys)
        logging.info(f"Upload status: {upload_status}")
    except Exception as e:
        logging.error(f"Error during file upload: {e}")

if __name__ == "__main__":
    main()