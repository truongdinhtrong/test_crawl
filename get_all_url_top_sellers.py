import re
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import os

site = 'https://tiki.vn/nha-sach-tiki/c8322?src=c.8322.hamburger_menu_fly_out_banner&order=top_seller'
base_url = 'https://tiki.vn'

response = requests.get(site)
page_content = BeautifulSoup(response.text)
elm = page_content.find('a', {'class': 'next'})
next_page_link = base_url + elm['href']

urls = ['https://tiki.vn/nha-sach-tiki/c8322?src=c.8322.hamburger_menu_fly_out_banner&order=top_seller']

i = True
while(i):
    time.sleep(2)
    with requests.get(urls[-1]) as r:
        page_content = BeautifulSoup(r.text)
        if page_content.find('a', {'class': 'next'}):
            elm = page_content.find('a', {'class': 'next'})
            next_page_link = base_url + elm['href']
            urls.append(next_page_link)
            print(next_page_link)
        else:
            i = False
            break

print(len(urls))

pwd_file = os.path.dirname(__file__)

df = pd.DataFrame(data={"url": urls})
df.to_csv(pwd_file + '/' + "urls.csv")

