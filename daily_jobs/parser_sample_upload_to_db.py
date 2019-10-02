from dao import FormParser

sample_parser = "edgar_parser_sample.py"
form_type = '13f-hr'

with open(sample_parser, 'rb') as f:
    data = f.read()

form_parser = FormParser()
form_parser.insert_parser(form_type, data)

retreived_code = form_parser.get_parser(form_type)

print(retreived_code)
