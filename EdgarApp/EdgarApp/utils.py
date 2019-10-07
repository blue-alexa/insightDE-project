import json
import gzip
from io import BytesIO

def gzip_json(data):
    byte_data = json.dumps(data).encode()
    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=6, fileobj=gzip_buffer)
    gzip_file.write(byte_data)
    gzip_file.close()
    return gzip_buffer.getvalue()

"""
from flask import Response

def get():
    ...
    content = gzip_json(data)
    response = Response(content, mimetype='application/gzip')
    return response
"""