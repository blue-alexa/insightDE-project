# SeeSEC
**A simple, powerful SEC Query API**

## Background
EDGAR database contains a wealth of information about the Commission and the securities industry which is freely available to the public. Information such as quarterly and yearly analysis of a public traded company, major share holders of a company, insider sells and buys etc, can be found in the filings of EDGAR database. It gives investors the ability to assess a company's history and progress, as well as make reasonable assumptions about its future through studying these filings. 

reference: [https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp](https://www.investopedia.com/articles/fundamental-analysis/08/sec-forms.asp)


## Features
* The SeeSEC API makes query EDGAR filings easy. A simple call gets historical 10-Q form filing information by Apple between 2008-01-01 and 2010-01-01 in json format.
[http://www.minimind.club/filing_index?cik=320193&form_type=10-Q&period1=20080101&period2=20100101](http://www.minimind.club/filing_index?cik=320193&form_type=10-Q&period1=20080101&period2=20100101)

* To query the content of filing documents, this call gets the 13F-HR forms that filed between 2019-07-01 and 2019-09-01 and contains MongoDB in its holdings in json format. This API currently only supports 13H-HR form content query, and can be extended to allow full text search of other types of forms in the future. 
[http://www.minimind.club/13f_search?cusip=60937P106&period1=20190701&period2=20190901](http://www.minimind.club/13f_search?cusip=60937P106&period1=20190701&period2=20190901)

* This API also provides user friendly web interface
[http://www.minimind.club](http://www.minimind.club)

## Pipeline
![alt text](https://drive.google.com/uc?export=view&id=1D0OmUFWqB4eSB3Bgd2Jz2LOOZTJAaBoT)

## Technical challenge
This project used Python Celery and RabbitMQ to build a distributed computing cluster to increase efficiency of batch processing of filing index documents and filing documents.





