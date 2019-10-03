import logging
import requests

def download(url):
    logger = logging.getLogger("BatchFilingManager.downloader")
    session = requests.Session()
    try:
        response = session.get(url)
    except Exception:
        logger.error(f"Failed to retreive data from {url}")

    if response.status_code == 200:
        content = response.content
        content = content.decode('ISO-8859-1')
        logger.info(f"Successfully downloaded from {url}")
        return content



