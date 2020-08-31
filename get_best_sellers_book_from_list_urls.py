import requests
import pandas as pd
import time, os, sys, re
from bs4 import BeautifulSoup
from datetime import datetime


def getDataUrls(url):
    #site = 'https://tiki.vn/nha-sach-tiki/c8322?src=c.8322.hamburger_menu_fly_out_banner&order=top_seller'
    response = requests.get(url)
    page_content = BeautifulSoup(response.text, 'html.parser')

    # B1 -------- Lấy title sách
    # lấy tất cả thẻ div sau đó lọc lại data theo 2 cách sau

    # Cách 01: tiki có add tên sách vào data-title nên dùng thẻ div lấy title sách
    # product_names = page_content.find_all('div')
    # titles = []
    # for i in range(len(product_names)):
    #     if product_names[i].has_attr('data-title'):
    #         titles.append(product_names[i]['data-title'])

    # Cách 02: 
    books = page_content.find_all('p', attrs={"class":"title"})
    list_of_titles = []
    for i in books:
        list_of_titles.append(i.text.strip())

    # B2 --- lấy giá sách:

    # ---- hàm lấy price:
    def get_price(str_price):
        price = 0
        str_price = (str_price.text).strip().split()
        if len(str_price) > 0:
            str_price = str_price[0].replace("đ", "")
        price = float(str_price.replace(".", ""))
        return price

    # ---- lấy tất cả thẻ p chứa price-sale:
    books = page_content.find_all('p', attrs={"class":"price-sale"})

    # ---- list price thường và price giảm giá:
    list_of_final_prices = []
    list_of_regular_prices = []

    prices = page_content.find_all('p', attrs={"class":"price-sale"})

    for section in prices:
        if section.find('span', 'final-price'):
            final = get_price(section.find('span', 'final-price'))
            list_of_final_prices.append(final)
        else:
            list_of_final_prices.append(0)
            
        if section.find('span', 'price-regular'):
            regular = get_price(section.find('span', 'price-regular'))
            list_of_regular_prices.append(regular)
        else:
            list_of_regular_prices.append(0)

    # B3 --- lấy link image:
    images = page_content.find_all('img', attrs={"class":"product-image img-responsive"})

    list_of_images = []
    for image in images:
        list_of_images.append(image["src"])

    # B4 --- tạo dataFrame --> save to file:
    if len(list_of_titles) == 0 and len(list_of_final_prices) == 0 and len(list_of_regular_prices) == 0 and len(list_of_images) == 0:
        print(url)
        print(len(list_of_titles), len(list_of_final_prices),len(list_of_regular_prices), len(list_of_images))
        print('Data doesn\'t exist !!!')
        pass
    else:
        print(url)
        print(len(list_of_titles), len(list_of_final_prices),len(list_of_regular_prices), len(list_of_images))

        pwd_file = os.path.dirname(__file__)
        stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        with open(pwd_file + '/' + 'temp.txt', 'a') as f:
            f.write('url: %s \n' % url)
            f.write('len: %s %s %s %s \n' % (len(list_of_titles), len(list_of_final_prices),len(list_of_regular_prices), len(list_of_images)))

        dictionary_books = {"title": list_of_titles,
                            "final_price": list_of_final_prices,
                            "regular_price": list_of_regular_prices,
                            'image': list_of_images}

        df = pd.DataFrame(dictionary_books)

        page_next = re.findall("page=[0-9]+", url)

        try:
            file_name = 'best_seller_books_' + stamp + '_' + page_next[0] +'.xlsx'
            df.to_excel(pwd_file + '/data/' + file_name, encoding='utf-8')
        except IndexError:
            file_name = 'best_seller_books_' + stamp + '_' + 'page=1' +'.xlsx'
            df.to_excel(pwd_file + '/data/' + file_name, encoding='utf-8')

        time.sleep(2)

if __name__ == "__main__":
    pwd_file = os.path.dirname(__file__)
    df = pd.read_csv(pwd_file + '/'+ "urls.csv")

    urls = []
    for i in df['url']:
        urls.append(i)

    # --- Get data
    for url in urls:
        getDataUrls(url)
