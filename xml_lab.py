import requests
from bs4 import BeautifulSoup
import json as js


class Base:
    def __init__(self, sitemap_url, json_name):
        self.book_list = []
        self.book_data = []
        self.sitemap = sitemap_url
        self.get_html()
        self.get_url_list()
        self.get_book_data()
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

    def get_book_data(self):
        NotImplemented

    def json_dump(self, json_name):
        with open(f"{json_name}.json", "w", encoding='utf8') as jsf:
            js.dump(self.book_data, jsf)
        jsf.close()


class Labirint(Base):

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

    def get_book_data(self):
        for book in self.book_list:
            html = get_html(book['book'])
            soup = BeautifulSoup(html, 'html.parser')
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
                country= None
            try:
                original_language = None
            except(AttributeError):
                original_language= None
            try:
                edition_language = None
            except(AttributeError):
                edition_language= None
            try:
                year_of_creating = None
            except(AttributeError):
                year_of_creating= None
            try:
                year_of_edition = ''.join(i for i in soup.find('div', class_='product-description').text if isdigit(i))
            except(AttributeError):
                year_of_edition= None
            try:
                ISBN =''.join(i for i in soup.find('div', class_='product-description').find('div', class_='isbn').text if isdigit(i))
            except(AttributeError):
                ISBN= None
            try:
                publishing =''.join(i for i in  soup.find('div', class_='product-description').find('div', class_='publisher').find('a').text if isalpha(i))
            except(AttributeError):
                publishing= None
            try:
                pages_count =''.join(i for i in soup.find('div', class_='product-description').find('div', class_='pages2').text[9:13] if isdigit(i))
            except(AttributeError):
                pages_count= None
            try:
                cover = soup.find('div', id='product-image').find('img')['src']
            except(AttributeError):
                cover= None
            try:
                scans = soup.find('img', class_='fotorama__img')
            except(AttributeError):
                scans= None
            try:
                annotation = soup.find('div', id='product-about').text
            except(AttributeError):
                annotation= None
            try:
                price = soup.find('span', class_='buying-priceold-val-number').text
            except(AttributeError):
                price= None
            try:
                sale_price = soup.find('span', class_='buying-pricenew-val-number').text
            except(AttributeError):
                sale_price= None
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
