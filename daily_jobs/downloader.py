import logging
import requests

def download(url):
    logger = logging.getLogger("es_feed.downloader")
    session = requests.Session()
    try:
        response = session.get(url)
    except Exception:
        logger.error(f"Failed to retreive data from {url}")

    if response.status_code == 200:
        content = response.content
        logger.info(f"Successfully downloaded from {url}")
        return content

    return None

def download_index(download_date):

    # synthesize download link
    quarter = (download_date.month - 1) // 3 + 1
    BASE_URL = 'https://www.sec.gov/Archives/edgar/daily-index/'
    filename = f"master.{download_date.strftime('%Y%m%d')}.idx"
    url = BASE_URL + f"{download_date.year}/QTR{quarter}/{filename}"

    content = download(url)
    return content
