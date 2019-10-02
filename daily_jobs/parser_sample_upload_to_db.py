import base64
from dao import FormParser

sample_parser = "edgar_parser_sample.py"
form_type = '13f-hr'

with open(sample_parser, 'rb') as f:
    data = f.read()

# encode func with base64 to avoid potential special character
encoded = base64.standard_b64encode(data).decode('ascii')

# write parser to db
form_parser = FormParser()
form_parser.insert_parser(form_type, encoded)

# read parser from db
retreived_code = form_parser.get_parser(form_type)
b_code = retreived_code.encode()
code = base64.standard_b64decode(b_code)

# test parser func works
exec(code)
print(EdgarFilingParser.doc_pattern)