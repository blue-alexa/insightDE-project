import argparse
import logging, os, glob
import boto3

from config import s3_filing_path, bucket_name

parser = argparse.ArgumentParser()
parser.add_argument('data_folder', help='Source folder of filing data')

val = parser.parse_args()
filing_path = val.data_folder

# create logger
logger = logging.getLogger("edgar_build.upload_to_s3")
s3 = boto3.resource('s3')

for f in glob.glob(filing_path + '/*.idx'):
    data = open(f, 'rb')
    key = os.path.join(s3_filing_path, os.path.basename(f))
    s3.Bucket(bucket_name).put_object(Key=key, Body=data)
    logger.info(f"Successfuly uploaded Filing {key} to S3")
