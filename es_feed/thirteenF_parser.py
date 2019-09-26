"""
parse xml (pick 13F-HR)
"""
import os, glob
import re
import json

import xmltodict

import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s - %(name)s - %(levelname)s - %(message)s'}
        },
    handlers = {
        'fh': {'class': 'logging.FileHandler',
               'formatter': 'f',
               'level': logging.INFO,
               'filename': 'es_feed_logger.log'},
        'ch': {'class': 'logging.StreamHandler',
               'formatter': 'f',
               'level': logging.INFO}
        },
    root = {
        'handlers': ['fh', 'ch'],
            'level': logging.INFO,
        }
)

dictConfig(logging_config)

# create logger
logger = logging.getLogger("es_feed.thirteenF_parser")


header_pattern = '<SEC-HEADER>(.*?)</SEC-HEADER>'
doc_pattern = '<XML>(.*?)</XML>'

source = '../edgar_data_download/data/thirteenF'
target_folder = '../edgar_data_download/data/thirteenF_json'
test = os.path.join(source, '0001172661-19-000001.txt')
test = os.path.join(source, '0000714364-19-000001.txt')

test_json = os.path.join(target_folder, '0001172661-19-000001.txt')
test_json = os.path.join(target_folder, '0000714364-19-000001.txt')



def parse_xml_to_json(filepath, target_folder):
    result = {}
    filename = os.path.basename(filepath)
    with open(filepath, 'r') as f:
        data = f.read()

    # print(data)
    m_header = re.search(header_pattern, data, re.DOTALL)
    if m_header:
        sec_header = m_header.group(0)
    else:
        pass
        # logger.error(f"SEC header is missing in {f}")

    docs = re.findall(doc_pattern, data[m_header.end():], re.DOTALL)

    for doc in docs:
        d = doc.strip()
        parsed_dict = xmltodict.parse(d, xml_attribs=False, process_namespaces=False)

        result.update(parsed_dict)

    target_file = os.path.join(target_folder, filename)
    with open(target_file, "w") as jsonfile:
        json_string = json.dumps(result)
        json_string = json_string.replace('"ns1:', '"') # clean up namespace tag if exists
        jsonfile.write(json_string)

        # json.dump(result, jsonfile)
        logger.info(f"Saved json to {target_file}")

for f in glob.glob(source + '/*.txt'):
    parse_xml_to_json(f, target_folder)

####### pretty print json data ##############
# with open(test_json, 'r') as f:
#     data = f.read()
# data = data.replace('"ns1:', '"') # remove namespace
# json_data = json.loads(data)
# print(json.dumps(json_data, indent=4, sort_keys=True))

"""
from lxml import etree
# context = etree.fromstring(doc)
# nsmap = context.nsmap.copy()
# print(nsmap[None])
# for elem in context.iter('*'):
#     print(elem.tag)
#     print(etree.QName(elem.tag).localname)
#     print(elem.text)

root = etree.fromstring(doc)

context = etree.iterwalk(root, events=("start", "end"))
for event, elem in context:

"""

