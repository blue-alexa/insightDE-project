import gzip
from io import BytesIO

def gzip_response(data):
    gzip_buffer = BytesIO()
    gzip_file = gzip.GzipFile(mode='wb', compresslevel=self.compress_level, fileobj=gzip_buffer)
    gzip_file.write(data)
    gzip_file.close()
    gzip_file.flush()
    return gzip_buffer.getvalue()
