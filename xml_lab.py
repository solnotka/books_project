import requests
from bs4 import BeautifulSoup
import json as js


class base_parsing:
    def __init__(self, sitemap_url, json_name):
        self.book_list = []
        self.sitemap = sitemap_url
        self.get_html()
        self.get_url_list()
        self.json_dump(json_name)


    def get_html(self, url=None):
        try:
            if url:
                result = requests.get(url)
            else:
                result = requests.get(self.sitemap)
            result.raise_for_status()
            self.sitemap_xml = result.text
        except(requests.RequestException, ValueError):
            return False

    def get_url_list(self):
        NotImplemented



    def json_dump(self, json_name):
        with open(f"{json_name}.json", "w", encoding='utf8') as jsf:
            js.dump(self.book_list, jsf)
        jsf.close()


class labirint_pars(base_parsing):

    def __init__(self):
        super().__init__()


    def get_url_list(self):
        soup = BeautifulSoup(self.sitemap_xml, 'xml')
        catalogs = soup.find_all('loc')
        self.res_list = []
        for catalog in catalogs:
            # cat_list.append(catalog.content)
            if 'smcatalog' in catalog.text:
                self.res_list.append(catalog.text)

        for res in self.res_list:
            html = self.get_html(url=res)
            soup = BeautifulSoup(self.sitemap_xml, 'xml')
            books = soup.find_all('loc')
            lastmod = soup.find_all('lastmod')
            for ind, book in enumerate(books):
                if 'books' in book.text:
                    book_url_mod = {'book': book.text, 'lastmod': lastmod[ind].text}
                    self.book_list.append(book_url_mod)
            print("Готово")

class book_data(labirint_pars):

    def get_book_data(book):
        html = get_html(book['book'])
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find('div', class_='product-description')
        title = soup.find('div', class_='prodtitle').find('h1').text
        author = data.find('div', class_='authors').find('a').text
        other_creators = None
        country = None
        original_language = None
        edition_language = None
        year_of_creating = None
        year_of_edition = data.find('div', class_='publisher').text[-7:-3]
        ISBN = data.find('div', class_='isbn').text[6:]
        publishing = data.find('div', class_='publisher').find('a').text
        pages_count = data.find('div', class_='pages2').text[9:13]
        cover = soup.find('div', id='product-image').find('img')['src']
        scans = soup.find('img', class_='fotorama__img')
        annotation = soup.find('div', id='product-about').text
        last_update = book['lastmod']
        shop_url = book['book']
        price = soup.find('span', class_='buying-priceold-val-number').text
        sale_price = soup.find('span', class_='buying-pricenew-val-number').text

        book_data = {
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
        }
        print(book_data)


labirint_pars('https://www.labirint.ru/sitemap.xml', 'labirint')

# def get_html(url):
#     try:
#         result = requests.get(url)
#         result.raise_for_status()
#         return result.text
#     except(requests.RequestException, ValueError):
#         return False
#
#
# def get_url_list(url):
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'xml')
#     catalogs = soup.find_all('loc')
#     res_list = []
#     for catalog in catalogs:
#         # cat_list.append(catalog.content)
#         if 'smcatalog' in catalog.text:
#             res_list.append(catalog.text)
#     return res_list
#
#
# def get_book_url(url):
#     html = get_html(url)
#     soup = BeautifulSoup(html, 'xml')
#     catalogs = soup.find_all('loc')
#     lastmod = soup.find_all('lastmod')
#     for ind, catalog in enumerate(catalogs):
#         book_url_mod = {}
#         if 'books' in catalog.text:
#             book_url_mod = {'book': catalog.text, 'lastmod': lastmod[ind].text}
#             book_list.append(book_url_mod)
#             print(book_list)
#     return print("Готово")
#
#
# list_cat = get_url_list('https://www.labirint.ru/sitemap.xml')
# book_list = []
# for cat in list_cat:
#     get_book_url(cat)
# with open("Labirint_url.json", "w", encoding='utf8') as jsf:
#     js.dump(book_list, jsf)
# jsf.close()



dict = {"book": "https://www.labirint.ru/books/746088/", "lastmod": "2020-09-26T01:45:47+03:00"}
get_book_data(dict)