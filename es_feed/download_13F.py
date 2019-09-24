import os, requests
from multiprocessing.pool import Pool

source = '../edgar_data_download/data/all_13F.txt'
target_folder = '..//edgar_data_download/data/thirteenF'

urls = []
with open(source, 'r') as f:
    for line in f:
        url = 'https://www.sec.gov/Archives/' + line.strip().split("|")[-1]
        urls.append(url)

def download_filing(url):

    def fetch(url):
        web_session = requests.Session()
        try:
            response = web_session.get(url)

            if response.status_code == 200:
                content = response.content
                return content

        except Exception:
            pass

        return None

    filename = url.split("/")[-1]
    filepath = os.path.join(target_folder, filename)

    content = fetch(url)
    if content:
        with open(filepath, 'wb') as f:
            f.write(content)
            print(f"Save to file {filepath}")

pool = Pool(processes=8)              # start 8 worker processes


for i in pool.imap_unordered(download_filing, urls):
    print(i)