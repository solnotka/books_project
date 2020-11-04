import requests
from bs4 import BeautifulSoup
import time
import random

from webapp import db
from webapp.small_model import Edition, Author, Publishing, Catalog, Shop

class Base:
    def __init__(self, sitemap_url):
        self.book_list = []
        self.books_data_set = []
        self.sitemap = sitemap_url
        self.get_html()
        self.get_url_list()
        self.get_book_data()

    def get_html(self, url=None):  # Извлекает html код из URl для дальнейшего использования.
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


class Labirint(Base):

    def get_url_list(self):  # Функция извлекающая ссылкни на каталоги из сайт мэпа и далее извлекающая ссылки на книги для дальнейшей обработки
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
            for book in books:
                if 'books' in book.text:
                    book_url_mod = book.text
                    self.book_list.append(book_url_mod)


    def get_book_data(self):
        for book in self.book_list:
            html = self.get_html(url=book)
            soup = BeautifulSoup(self.sitemap_xml, 'html.parser')
            
            try:
                authors_list = []
                author_first = soup.find('div', class_='authors').find_all('a', class_='analytics-click-js', attrs={'data-event-label': "author"})
                for a in author_first:
                    authors_list.append(a.text.strip(). replace('  ', ' '))
                if authors_list:
                    author_check = authors_list[0].split()
            except(AttributeError):
                authors_list = None

            try:
                title_first = soup.find('div', class_='prodtitle').find('h1').text
                title_second = title_first.split(':')
                if author_check and author_check[0] in title_second[0]:
                    title = (''.join(title_second[1:])).strip().replace('  ', ' ')
                else:
                    title = title_first.strip()
            except(AttributeError):
                title = None

            try:
                year_of_edition = ''.join(
                    i for i in soup.find('div', class_='product-description').find('div', class_='publisher').text
                    if i.isdigit())
            except(AttributeError):
                year_of_edition = None

            try:
                ISBN_first = soup.find('div', class_='isbn').text
                ISBN = (ISBN_first.replace('ISBN:', '')).strip()
                if len(ISBN) > 17:
                    for digit in ISBN:
                        if digit.isalpha():
                            ISBN = ISBN.replace(digit, '')
                    ISBN = ISBN.split(',')
                    for i in range(len(ISBN)):
                        ISBN[i] = ISBN[i].strip()
            except(AttributeError):
                ISBN = None

            try:
                publishing = soup.find('div', class_='publisher').find('a', class_='analytics-click-js', attrs={'data-event-label': "publisher"}).text.replace('  ', ' ')
            except(AttributeError):
                publishing = None

            try:
                cover = soup.find('div', id='product-image').find('img')['src']
            except(AttributeError):
                cover = None
            
            try:
                annotation_first = soup.find('div', id='product-about').find('div', id='fullannotation')
                if not annotation_first:
                    annotation = soup.find('div', id='product-about').find('p').text.replace('  ', ' ')
                else:
                    annotation = annotation_first.find('p').text.replace('  ', ' ')
            except(AttributeError):
                annotation = None

            try:
                price = soup.find('span', class_='buying-priceold-val-number').text + ' руб'
            except(AttributeError):
                price = "Неизвестно"
            
            url = book

            book_data = {
                        'title': title,
                        'authors_list': authors_list,
                        'year_of_edition': year_of_edition,
                        'ISBN': ISBN,
                        'publishing': publishing,
                        'cover': cover,
                        'annotation': annotation,
                        'url': url,
                        'price': price,
                        }
            self.books_data_set.append(book_data)


def save_lab_books(url):
    # Эта функция позволяет последовательно заполнить таблицы базы в следующем порядке: Publishing,
    # Shop, Edition (нельзя заполнить без Publishing), Author (в процессе устанавливается связь между авторами и изданиями),
    # Catalog (можно создать только при заполненном издании)

    res = Labirint(url)
    books_list = res.books_data_set

    def save_edition(book, ISBN):
        edition_exists = Edition.query.filter(Edition.ISBN == ISBN).count()
        if not edition_exists:
            title = book['title']
            year_of_edition = book['year_of_edition']
            ISBN = ISBN
            cover = book['cover']
            annotation = book['annotation']
            publishing = new_publishing.id
            new_edition = Edition(title=title,
                                  year_of_edition=year_of_edition, ISBN=ISBN,
                                  cover=cover, annotation=annotation,
                                  publishing=publishing)
            db.session.add(new_edition)
            db.session.commit()
        else:
            new_edition = Edition.query.filter_by(ISBN=ISBN).first()
        return new_edition

    shop_exists = Shop.query.filter(Shop.name == 'Лабиринт').count()
    if not shop_exists:
        new_shop = Shop(name='Лабиринт', logo='https://img.labirint.ru/design/logomini.png', url='https://www.labirint.ru/')
        db.session.add(new_shop)
        db.session.commit()
    else:
        new_shop = Shop.query.filter_by(name='Лабиринт').first()

    for book in books_list:
        publishing_exists = Publishing.query.filter(Publishing.name == book['publishing']).count()
        if not publishing_exists:
            new_publishing = Publishing(name=book['publishing'])
            db.session.add(new_publishing)
            db.session.commit()
        else:
            new_publishing = Publishing.query.filter_by(name='ДМК Пресс').first()
        
        if type(book['ISBN']) == 'list':
            new_edition = save_edition(book, book['ISBN'][-1])
        else:
            new_edition = save_edition(book, book['ISBN'])    

        for author in book['authors_list']:
            author_exists = Author.query.filter(Author.pseudonim == author).count()
            if not author_exists:
                new_author = Author(pseudonim=author, real_name=author)
                db.session.add(new_author)
                db.session.commit()
            else:
                new_author = Author.query.filter_by(pseudonim=author).first()
            new_author.editions.append(new_edition)

        item_exists = Catalog.query.filter(Catalog.url == book['url']).count()
        if not item_exists:
            new_catalog = Catalog(book=new_edition.id,
                                  point_of_sell=new_shop.id,
                                  price=book['price'], url=book['url'])
            db.session.add(new_catalog)
            db.session.commit()
        else:
            new_catalog = Catalog.query.filter_by(url=book['url']).first()
            new_catalog.price = book['price']