import os
import logging
import requests

def download_filing(param):
    """
    download designated file from SEC website.
    :param param: (filedate: datetime.date object, path: path to store file)
    """

    def fetch(url, filename):
        web_session = requests.Session()
        try:
            response = web_session.get(url)

            if response.status_code == 200:
                content = response.content  # content in bytes format
                module_logger.info(f"Succeeded to download {filename} from link {url}")
                return content
            else:
                module_logger.error(
                    f"Failed to download {filename} from link {url}, status code: {response.status_code}")
                raise RuntimeError()
        except Exception:
            module_logger.error(f"Failed to download {filename} from link {url}", exc_info=True)
            raise RuntimeError

    module_logger = logging.getLogger("filing_download.filing_downloader")

    filedate, path = param
    # synthesize download link
    quarter = (filedate.month - 1) // 3 + 1
    BASE_URL = 'https://www.sec.gov/Archives/edgar/daily-index/'
    filename = f"master.{filedate.strftime('%Y%m%d')}.idx"
    url = BASE_URL + f"{filedate.year}/QTR{quarter}/{filename}"

    # download file from sec website
    try:
        content = fetch(url, filename)
    except RuntimeError as e:
        return

    filepath = os.path.join(path, filename)

    with open(filepath, 'wb') as f:
        f.write(content)

    return f"Succeeded to download {filename} from link"
