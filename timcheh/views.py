import time

from django.http import HttpResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_BS(url):
    html = urlopen('https://timcheh.com{}'.format(url))
    bs = BeautifulSoup(html, 'html.parser')
    return bs


def crawl_pages():
    page_num = 1
    products_list = []
    all_links = []

    main_url = '/search/category-mobile?page='
    url = main_url + str(page_num)
    bs = get_BS(url)

    while bs.find('div', 'styles_alert__1Js-r') is None:

        time.sleep(1)

        # crawl names
        names_list = []
        names = bs.find_all('h3', {'class': 'styles_title__20lcD'})

        for name in names:
            names_list.append(name.get_text())

        # crawl prices
        prices_list = []
        prices = bs.find_all('div', {'class': 'styles_price__cldWW'})

        for price in prices:
            prices_list.append(int((price.get_text()).replace(',', '')))

        # crawl links
        links_list = []
        links = bs.find_all('a', {'class': 'styles_product_card__1y61Y styles_hover_style__KdhHU'})

        for link in links:
            links_list.append(link.attrs['href'])
            all_links.append(link.attrs['href'])

        list_information = {
            'names': names_list,
            'prices': prices_list,
            'links': links_list,
        }

        products_list.append(list_information)

        page_num += 1
        url = main_url + str(page_num)
        bs = get_BS(url)

    return all_links


def source_products(request):
    links = crawl_pages()

    products_info = []

    for link in links:
        bs = get_BS(link)

        # crawl product name
        name = bs.find('h1', {'class': 'product_styles_product_title__2NMTI'}).get_text()

        # crawl product price
        price = bs.find('span', 'product_styles_price__3Ws3t').get_text()
        try:
            price = int(price.replace(',', ''))
        except:
            price = 0

        list_information = {
            'name': name,
            'prices': price,
        }

        products_info.append(list_information)

    return HttpResponse([products_info])
