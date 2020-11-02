import requests
from bs4 import BeautifulSoup
import json as js
import time
import random


class Base:
    def __init__(self, sitemap_url, json_name):
        self.book_list = []
        self.book_data = []
        self.sitemap = sitemap_url
        self.get_html()
        self.get_ua()
        self.get_proxy()
        self.get_hide_html()
        self.get_url_list()
        self.get_book_data()
        self.json_dump(json_name)

    def get_html(self, url=None):  # Извлекает html код из URl , для дальнейшего использования.
        try:
            if url:
                result = requests.get(url)
            else:
                result = requests.get(self.sitemap)
            result.raise_for_status()
            self.sitemap_xml = result.text
        except(requests.RequestException, ValueError):
            return False

    def get_hide_html(self, url=None):  # Извлекает html код из URl , для дальнейшего использования.
        try:
            result = requests.get(url, headers=self.get_ua(), proxies=self.get_proxy())
            result.raise_for_status()
            self.hide_html = result.text
        except(requests.RequestException, ValueError):
            return False

    def get_proxy(self):  # Получение прокси
        try:
            result = requests.get('http://pubproxy.com/api/proxy')
            result.raise_for_status()
            proxy = {'http': 'http://' + result.json()["data"][0]['ipPort']}
            return proxy
        except(requests.RequestException, ValueError):
            return False

    def get_ua(self):  # Генератор User Agent
        i = random.randint(10, 99)
        j = random.randint(1000, 9999)
        k = random.randint(1000, 9999)
        pc = ["(Windows NT 6.1; WOW64)",
              "(Windows NT 6.1; WOW64)",
              "(Macintosh; Intel Mac OS X 10_10)",
              "(Windows NT 6.1; WOW64; rv:33.0)",
              "(Windows NT 6.3; WOW64)",
              "(Macintosh; Intel Mac OS X 10_10_0)",
              "(Macintosh; Intel Mac OS X 10_9_5)",
              "(Windows NT 6.1; WOW64; Trident/7.0; rv:11.0)",
              "(Windows NT 6.3; WOW64; rv:33.0)",
              "(Windows NT 6.1; WOW64)"
              ]
        f = random.choice(pc)
        ua = {
            'User-Agent': f'Mozilla/5.0 {f} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{i}.0.{j}.121 Safari/537.36 OPR/71.0.{k}.234'}
        return ua

    def get_url_list(self):
        NotImplemented

    def get_book_data(self):
        NotImplemented

    def json_dump(self, json_name):
        with open(f"{json_name}.json", "w", encoding='utf8') as jsf:
            js.dump(self.book_data, jsf)
        jsf.close()


class Labirint(Base):

    def get_url_list(
            self):  # Функиция извлекающая ссылкни на каталоги из сайт мэпа и далее извлекающая ссылки на книги для дальнейшей обработки
        soup = BeautifulSoup(self.sitemap_xml, 'xml')  # Извлечение списка каталогов
        catalogs = soup.find_all('loc')
        self.res_list = []
        for catalog in catalogs:
            if 'smcatalog' in catalog.text:
                self.res_list.append(catalog.text)

        for res in self.res_list:
            self.get_html(url=res)
            soup = BeautifulSoup(self.sitemap_xml, 'xml')
            books = soup.find_all('loc')
            lastmod = soup.find_all('lastmod')
            for ind, book in enumerate(books):
                if 'books' in book.text:
                    book_url_mod = {'book': book.text, 'lastmod': lastmod[ind].text}
                    self.book_list.append(book_url_mod)
            print("Готово")

    def get_book_data(self):
        for book in self.book_list:
                html = self.get_html(url=book['book'])
                soup = BeautifulSoup(self.sitemap_xml, 'html.parser')
                try:
                    title = soup.find('div', class_='prodtitle').find('h1').text
                except(AttributeError):
                    title = None
                try:
                    author = soup.find('div', class_='product-description').find('div', class_='authors').find('a').text
                except(AttributeError):
                    author = None
                try:
                    other_creators = None
                except(AttributeError):
                    other_creators = None
                try:
                    country = None
                except(AttributeError):
                    country = None
                try:
                    original_language = None
                except(AttributeError):
                    original_language = None
                try:
                    edition_language = None
                except(AttributeError):
                    edition_language = None
                try:
                    year_of_creating = None
                except(AttributeError):
                    year_of_creating = None
                try:
                    year_of_edition = ''.join(
                        i for i in soup.find('div', class_='product-description').find('div', class_='publisher').text
                        if i.isdigit())
                except(AttributeError):
                    year_of_edition = None
                try:
                    ISBN = ''.join(
                        i for i in soup.find('div', class_='product-description').find('div', class_='isbn').text if
                        i.isdigit())
                except(AttributeError):
                    ISBN = None
                try:
                    publishing = ''.join(i for i in soup.find('div', class_='product-description').find('div',
                                                                                                        class_='publisher').find(
                        'a').text if i.isalpha())
                except(AttributeError):
                    publishing = None
                try:
                    pages_count = ''.join(
                        i for i in soup.find('div', class_='product-description').find('div', class_='pages2').text if
                        i.isdigit())
                except(AttributeError):
                    pages_count = None
                try:
                    cover = soup.find('div', id='product-image').find('img')['src']
                except(AttributeError):
                    cover = None
                try:
                    scans = soup.find('img', class_='fotorama__img')
                except(AttributeError):
                    scans = None
                try:
                    annotation = soup.find('div', id='product-about').find('div', id='fullannotation').find('p').text
                except(AttributeError):
                    annotation = None
                try:
                    price = soup.find('span', class_='buying-priceold-val-number').text
                except(AttributeError):
                    price = None
                try:
                    sale_price = soup.find('span', class_='buying-pricenew-val-number').text
                except(AttributeError):
                    sale_price = None
                last_update = book['lastmod']
                shop_url = book['book']

                book_data = {'title': title, 'data': {
                    'title': title,
                    'author': author,
                    'other_creators': other_creators,
                    'country': country,
                    'original_language': original_language,
                    'edition_language': edition_language,
                    'year_of_creating': year_of_creating,
                    'year_of_edition': year_of_edition,
                    'ISBN': ISBN,
                    'publishing': publishing,
                    'pages_count': pages_count,
                    'cover': cover,
                    'scans': scans,
                    'annotation': annotation,
                    'last_update': last_update,
                    'shop_url': shop_url,
                    'price': price,
                    'sale_price': sale_price
                }}
                self.book_data.append(book_data)
        print(self.book_data)


class Chitai(Base):
    def get_url_list(self):
        soup = BeautifulSoup(self.sitemap_xml, 'xml')
        catalogs = soup.find_all('loc')
        self.res_list = []
        for catalog in catalogs:
            if 'goods' in catalog.text:
                self.res_list.append(catalog.text)

        for res in self.res_list:
            html = self.get_html(url=res)
            soup = BeautifulSoup(self.sitemap_xml, 'xml')
            books = soup.find_all('loc')
            lastmod = soup.find_all('lastmod')
            for ind, book in enumerate(books):
                if 'book' in book.text:
                    book_url_mod = {'book': book.text, 'lastmod': lastmod[ind].text}
                    self.book_list.append(book_url_mod)
            print("Готово")

    def get_book_data(self):
        start_time = time.time()
        for book in self.book_list:
            html = self.get_hide_html(url=book['book'])
            soup = BeautifulSoup(self.sitemap_xml, 'html.parser')
            try:
                title = soup.find('h1', class_="product__title js-analytic-product-title").text.strip()
            except(AttributeError):
                title = None
            try:
                author = soup.find('a', class_='link product__author').text.strip().split(',')
            except(AttributeError):
                author = None

            data = {}
            data_soup = soup.find("div", class_="product__props").findAll('div', class_="product-prop")
            for el in data_soup:
                data[f"{el.find('div', class_='product-prop__title').text.strip()}"] = el.find('div',
                                                                                               class_="product-prop__value").text.strip()
            publishing = data.get('Издательство', None)
            year_of_edition = data.get('Год издания', None)
            isISBN = data.get('ISBN', None)
            if isISBN:
                ISBN = "".join(i for i in isISBN if i.isdigit())
            else:
                ISBN = None
            pages_count = data.get('Кол-во страниц', None)
            try:
                cover = soup.find('div', class_="product__image").find('img')['data-src']
            except(AttributeError):
                cover = None
            try:
                annotation = soup.find('div', itemprop="description").text.strip()
            except(AttributeError):
                annotation = None
            try:
                price = ''.join(
                    i for i in soup.find('div', class_="product__price").find('div', class_='price').text if
                    i.isdigit())
            except(AttributeError):
                price = None
            try:
                scans = & & &
                except(AttributeError):
                scans = None
            country = None
            original_language = None
            edition_language = None
            year_of_creating = None
            sale_price = None

            book_data = {'title': title, 'data': {
                'title': title,
                'author': author,
                'other_creators': None,
                'country': country,
                'original_language': original_language,
                'edition_language': edition_language,
                'year_of_creating': year_of_creating,
                'year_of_edition': year_of_edition,
                'ISBN': ISBN,
                'publishing': publishing,
                'pages_count': pages_count,
                'cover': cover,
                'scans': scans,
                'annotation': annotation,
                'price': price,
                'sale_price': sale_price
            }}
        self.book_data.append(book_data)


And = Labirint('https://www.labirint.ru/sitemap.xml', 'labirint')
