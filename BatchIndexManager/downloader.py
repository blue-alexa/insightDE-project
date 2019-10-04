import logging
import requests

def download(url):
    logger = logging.getLogger("BatchIndexManager.downloader")
    session = requests.Session()
    try:
        response = session.get(url)
    except Exception:
        logger.error(f"Failed to retreive data from {url}")

    if response.status_code == 200:
        content = response.content
        content = content.decode('ISO-8859-1') # decode with lain-1
        logger.info(f"Successfully downloaded from {url}")
        return content

    return None

def download_index(download_date):
    """
    download index file of particular date
    :param download_date: datetime object
    :return:
    """
    # synthesize download link
    quarter = (download_date.month - 1) // 3 + 1
    BASE_URL = 'https://www.sec.gov/Archives/edgar/daily-index/'
    filename = f"master.{download_date.strftime('%Y%m%d')}.idx"
    url = BASE_URL + f"{download_date.year}/QTR{quarter}/{filename}"

    content = download(url)
    return content