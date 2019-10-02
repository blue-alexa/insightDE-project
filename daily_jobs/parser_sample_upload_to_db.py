import base64
from dao import FormParser

sample_parser = "edgar_parser_sample.py"
form_type = '13f-hr'

with open(sample_parser, 'rb') as f:
    data = f.read()

encoded_data = base64.b64encode(data)

form_parser = FormParser()
form_parser.insert_parser(form_type, encoded_data)

retreived_code = form_parser.get_parser(form_type)
code = base64.b64decode(retreived_code)

print(code)
