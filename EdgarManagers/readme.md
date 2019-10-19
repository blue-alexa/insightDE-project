EdgarManagers module implements:
1. Batch processing for historical data
1. Running daily jobs

To run batch processing on filing meta data, please run `batch_filing_index.py` on Celery executor.

To run batch processing on 13F-HR filing documents, please run `batch_filings.py` on Celery executor.

To initialize ElasticSearch index and mapping, please run `init_es.py`.

To run daily jobs for retrieving and processing index file and filing documents, please run `daily_jobs.py` on Celery executor.

To start Celery workers, please run the following script on every Celery worker: `celery -A tasks worker -f <logfile> --loglevel=info`

To add a customized parser class, please create a class derived from class `AbstractFormParser` and implement function `parse(source, source_name)`, name the file as `FormParser_<form-type>.py` and save it in the EdgarManagers/edgar_parsers folder. 

Workflow of daily job:
![alt text](https://drive.google.com/open?id=1yo36t4VtcRRTnd5nRA0QcFXY75xsrult)