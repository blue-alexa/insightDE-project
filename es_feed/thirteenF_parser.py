import os, glob
import re
import xml.etree.ElementTree as ET

# from xml.etree.ElementTree import parse

header_pattern = '<SEC-HEADER>(.*?)</SEC-HEADER>'
doc_pattern = '<XML>(.*?)</XML>'

source = '../edgar_data_download/data/thirteenF'
test = os.path.join(source, '0001172661-19-000001.txt')
with open(test, 'r') as f:
    data = f.read()

# print(data)
m_header = re.search(header_pattern, data, re.DOTALL)
if m_header:
    sec_header = m_header.group(0)
else:
    pass
    # logger.error(f"SEC header is missing in {f}")

docs = re.findall(doc_pattern, data[m_header.end():], re.DOTALL)
doc = docs[1].strip()

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



