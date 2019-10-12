import logging
import requests
from datetime import datetime

def download(url):
    logger = logging.getLogger("DailyJobs.downloader")
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
    :param download_date: str YYYYMMDD
    :return:
    """
    d = datetime.strptime(download_date, "%Y%m%d")
    # synthesize download link
    quarter = (d.month - 1) // 3 + 1
    BASE_URL = 'https://www.sec.gov/Archives/edgar/daily-index/'
    filename = f"master.{download_date}.idx"
    url = BASE_URL + f"{d.year}/QTR{quarter}/{filename}"

    content = download(url)
    return content
