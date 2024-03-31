import requests
from bs4 import BeautifulSoup

URL = "https://pyony.com/brands/gs25/?page=1&event_type=&category=&item=100&sort=&price=&q="

def get_max_page(URL : str):
    response = requests.get(URL)

    soup = BeautifulSoup(response.content, 'html.parser')

    page_div = soup.find("ul", "pagination pagination-sm").find_all("li")[-1]
    
    max_page = page_div.a['href'].split("&")[0].split("=")[-1]

    return int(max_page)

def get_product_with_pages(page_num : int):
    URL_with_page = f"https://pyony.com/brands/gs25/?page={page_num}&event_type=&category=&item=100&sort=&price=&q="
    res = requests.get(URL_with_page)

    soup = BeautifulSoup(res.content, 'html.parser')

    product_div = soup.select("body > div > div > div.col-md-12.col-lg-8 > div.row")

    for product_element in product_div[0].find_all("div", "col-md-6"):
        get_product_detail(product_element)

def get_product_detail(product_div):
    texts = product_div.select("a > div > div.card-body.px-2.py-2 > div:nth-child(2)")[0].text

    text_list = list()

    for text in texts.split("\n"):
        text = text.strip()
        if text:
            text_list.append(text)

    del text_list[4:6]
    
    product_list.append(text_list)

def write_csv(product_list_para : list):
    import csv

    f = open('product.csv', 'w', newline='')
    wr = csv.writer(f)

    wr.writerow(["제품", "원가격", "할인된 가격", "행사 내용"])

    for product in product_list_para:
        wr.writerow(product)
    
    f.close()

    
product_list = list()

max_page = get_max_page(URL)

for i in range(1, max_page + 1):
    get_product_with_pages(i)
    
write_csv(product_list)