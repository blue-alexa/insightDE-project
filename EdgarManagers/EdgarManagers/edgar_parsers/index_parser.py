import logging
from datetime import datetime

index_parser_logger = logging.getLogger("DailyJobs.index_parser")

class IndexParser(object):
    def __init__(self):
        pass

    def _clean(self, entry):
        entry = entry.strip()
        if "\\" in entry:
            entry = entry.replace("\\", "\\\\")
        if "'" in entry:
            entry = entry.replace("'", "''")
        return entry

    def parse(self, data, download_date):
        """
        :param data: must be decoded to ISO-8859-1
        :param download_date: YYYYMMDD
        :return: list of tuples (cik, company_name, form_type, date_filed, accession_no, url)
        (str, str, str, str, str, str)
        """
        records = []
        lines = data.split('\n')
        lines = lines[7:] # Skip first 7 lines of header

        for line in lines:
            data = line.strip().split("|")
            if len(data) == 5:
                for i, elem in enumerate(data):
                    data[i] = self._clean(elem)

                try:
                    data[3] = datetime.strptime(data[3], "%Y%m%d").strftime("%Y-%m-%d")
                except ValueError:
                    index_parser_logger.error(f"Failed to process time in line: {line}")
                    data[3] = datetime.strptime(download_date, "%Y%m%d").strftime("%Y-%m-%d")

                cik, company_name, form_type, date_filed, filing_content = data
                accession_no = filing_content.split("/")[-1].split(".")[0] # get accession number
                url = 'https://www.sec.gov/Archives/'+filing_content

                records.append((cik, company_name, form_type, date_filed, accession_no, url))

        return records