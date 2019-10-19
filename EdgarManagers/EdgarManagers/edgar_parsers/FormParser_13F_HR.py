import re
import logging

from lxml import etree

from FormParser import AbstractFormParser

F13_parser_logger = logging.getLogger("DailyJobs.FormParser_13F_HR")

class FormParser_13F_HR(AbstractFormParser):
    header_pattern = '<SEC-HEADER>(.*?)</SEC-HEADER>'
    doc_pattern = '<XML>(.*?)</XML>'

    def __init__(self):
        pass

    def _get_header_info(self, header):
        lines = header.split("\n")
        for line in lines:
            if "COMPANY CONFORMED NAME:" in line:
                company_name = line.split(":")[1].strip()

            if "CONFORMED PERIOD OF REPORT:" in line:
                report_date = line.split(":")[1].strip()
                report_date = report_date[0:4]+'-'+report_date[4:6]+'-'+report_date[6:8] #date format YYYY-MM-DD

            if "FILED AS OF DATE:" in line:
                file_date = line.split(":")[1].strip()
                file_date = file_date[0:4]+'-'+file_date[4:6]+'-'+file_date[6:8]

            if "CENTRAL INDEX KEY:" in line:
                cik = line.split(":")[1].strip()

        return {'company_name': company_name, 'report_date': report_date, 'file_date': file_date, 'cik': cik}

    def _get_holding_info(self, data):
        """
        Extracting positions info from 13F
        :param data:
        :return:
        """
        holdings = []
        docs = re.findall(self.doc_pattern, data, re.DOTALL)
        for doc in docs:
            doc = doc.strip()
            if doc.startswith("<?xml"):
                doc = re.sub('<\?xml(.*?)>', '', doc)

            try:
                context = etree.fromstring(doc)
            except Exception as e:
                print(e)
                continue

            if not doc:
                continue

            for elem in context.iter('{*}infoTable'):
                holding = {}
                try:
                    issuer = elem.find("{*}nameOfIssuer")
                    holding['nameOfIssuer'] = issuer.text
                    title = elem.find("{*}titleOfClass")
                    holding['titleOfClass'] = title.text
                    cusip = elem.find("{*}cusip")
                    holding['cusip'] = cusip.text
                    value = elem.find("{*}value")
                    holding['value'] = value.text
                    shrsOrPrnAmt = elem.find("{*}shrsOrPrnAmt")
                    sshPrnamt = shrsOrPrnAmt.find("{*}sshPrnamt")
                    sshPrnamtType = shrsOrPrnAmt.find("{*}sshPrnamtType")
                    holding['shrsOrPrnAmt'] = {'sshPrnamt': sshPrnamt.text, 'sshPrnamtType': sshPrnamtType.text}
                except AttributeError:
                    pass
                if holding:
                    holdings.append(holding)
        return holdings

    def parse(self, source, source_name):
        """
        :param source: xml file
        :param source_name: string, any name, could be accession_no or url, for logging purpose
        :return: json object for elastic search to load, one xml document generate one json object
        """
        self.source = source
        self.source_name = source_name
        entry = {}
        m_header = re.search(self.header_pattern, self.source, re.DOTALL)
        if m_header:
            sec_header = m_header.group(0)
        else:
            F13_parser_logger.error(f"No SEC header in {self.source_name}")
            return

        header = self._get_header_info(sec_header)
        holdings = self._get_holding_info(source[m_header.end():])
        entry.update(header)
        if holdings:
            entry.update({"holdings": holdings})
            F13_parser_logger.info(f"Successfully retrieve holding information from {self.source_name}")
        else:
            F13_parser_logger.error(f"Can not find holding information in {self.source_name}")
            return

        return entry
