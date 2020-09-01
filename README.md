# Test Crawl

## install python 3.6 from CentOS:

yum install gcc bzip2-devel libffi-devel openssl-devel 

./configure --enable-optimizations 
  
make altinstall 

## install pandas:

pip3.6 install pandas

## how it works

1. Get all links best sellers:
pytyhon3.6 get_all_url_top_sellers.py

2. Get all data from list urls.csv
pytyhon3.6 get_best_sellers_book_from_list_urls.py

3. Combine all file data excel to dataset:
pytyhon3.6 combine_all_file_data_excel.py
