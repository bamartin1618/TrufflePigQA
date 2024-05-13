import logging
from urllib.parse import urlparse, urljoin, urldefrag
import tldextract

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def domain_match(url1, url2):
    """
    Check if the domains of the two URLs match.

    Args:
        url1 (str): The first URL.
        url2 (str): The second URL.

    Returns:
        bool: True if the domains match, False otherwise.
    """
    domain1 = tldextract.extract(url1).registered_domain
    domain2 = tldextract.extract(url2).registered_domain
    return domain1 == domain2

def is_valid_url(url, parent_link):
    """
    Check if the URL is valid, belongs to the same domain as the parent link, and is not a fragment.

    Args:
        url (str): The URL to validate.
        parent_link (str): The parent link for domain comparison.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        parsed_url = urlparse(url)
        if not parsed_url.scheme or not parsed_url.netloc:
            logger.warning(f"Invalid URL scheme or netloc: {url}")
            return False
        if not domain_match(url, parent_link):
            logger.warning(f"Domain mismatch: {url} and {parent_link}")
            return False
        if parsed_url.fragment:
            logger.info(f"URL is a fragment: {url}")
            return False
        return True
    except ValueError as e:
        logger.error(f"Error parsing URL: {url} - {e}")
        return False

def normalize_url(base, link):
    """
    Normalize a URL by resolving it against a base URL and removing any fragments.

    Args:
        base (str): The base URL.
        link (str): The URL to normalize.

    Returns:
        str: The normalized URL, or None if an error occurs.
    """
    try:
        joined_url = urljoin(base, link)
        defragmented_url, _ = urldefrag(joined_url)
        return defragmented_url
    except ValueError as e:
        logger.error(f"Error normalizing URL: {link} with base {base} - {e}")
        return None