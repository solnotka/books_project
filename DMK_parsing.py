import requests

from bs4 import BeautifulSoup
from webapp import db
from webapp.small_model import Edition, Author, Publishing, Catalog, Shop
def get_url_list(sitemap_url):
    soup = BeautifulSoup(sitemap_url.text, 'xml')
    catalogs = soup.find_all('loc')
    res_list = []
    for catalog in catalogs:
        if '978-5-' in catalog.text:
            res_list.append(catalog.text)
    return res_list


def get_book_data(res_list):
    books_list = []
    for url in res_list:
        soup_html = BeautifulSoup(requests.get(url).text)
        title = soup_html.find('h1').text

        # Это страховка на случай отсутствия информации
        ISBN = ''
        authors_list = []
        year_of_edition = ''

        # Основная информация записана в общий div. Класс не является
        # уникальным опознавательным признаком этого блока, поэтому его приходится
        # искать по ключевому слову (ISBN).

        info = soup_html.find_all('div', class_='span4')
        for info_block in info:
            if 'ISBN' in str(info_block):
                info_list = str(info_block.text).split(':')
        for i in range(len(info_list)):
            if 'Автор' in info_list[i]:
                authors = (info_list[i + 1]).replace('Дата выхода', '').replace('Формат', '')
                authors_list = str(authors).split(',')
                for i in range(len(authors_list)):
                    authors_list[i] = authors_list[i].strip()
            if 'Дата выхода' in info_list[i]:
                year_of_edition = info_list[i + 1]
                for letter in year_of_edition:
                    if not letter.isdigit():
                        year_of_edition = year_of_edition.replace(letter, '')
            if 'ISBN' in info_list[i]:
                ISBN = info_list[i + 1]
                for number in ISBN:
                    if number.isalpha():
                        ISBN = ISBN.replace(number, '')
                ISBN = ISBN.strip()

        annotation_card = soup_html.find('div', class_='card-note')
        if annotation_card:
            annotation = (str(annotation_card.text).replace('Аннотация', '')).strip()
        else:
            annotation = 'Аннотация не найдена'

    # На странице не полная ссылка на фото, поэтому приходится ее дополнять вручную.
    # Мне нужно содержимое тега src, поэтому я обращаюсь к нему как к словарю.
        cover_first = soup_html.find('div', class_='cart-img-big')
        if cover_first:
            cover_second = cover_first.find('img')
        if cover_second:
            cover = 'https://dmkpress.com' + cover_second['src']
        else:
            cover = 'Обложка не найдена'

        price_first = soup_html.find('div', class_='card-price')
        if price_first:
            price = str(price_first.find('div').text).strip()
        else:
            price = 'Неизвестно'

        book = {'url': url, 'title': title, 'authors_list': authors_list,
                'year_of_edition': year_of_edition, 'ISBN': ISBN,
                'annotation': annotation, 'cover': cover, 'price': price}
        
        books_data_set.append(book)
    
    return books_list


def save_books(url):
    # Эта функция позволяет последовательно заполнить таблицы базы в следующем порядке: Publishing,
    # Shop, Edition (нельзя заполнить без Publishing), Author (в процессе устанавливается связь между авторами и изданиями),
    # Catalog (можно создать только при заполненном издании)

    res_list = get_url_list(url)
    books_list = get_book_data(res_list)

    publishing_exists = Publishing.query.filter(Publishing.name == 'ДМК Пресс').count()
    if not publishing_exists:
        new_publishing = Publishing(name='ДМК Пресс', logo='https://dmkpress.com/templates/dmk/images/logo.png',
                                    town='Москва', url='https://dmkpress.com/',
                                    adress='115487, г. Москва, Пр-т Андропова, д. 38')
        db.session.add(new_publishing)
        db.session.commit()
    else:
        new_publishing = Publishing.query.filter_by(name='ДМК Пресс').first()
    
    shop_exists = Shop.query.filter(Shop.name == 'ДМК Пресс').count()
    if not shop_exists:
        new_shop = Shop(name='ДМК Пресс', logo='https://dmkpress.com/templates/dmk/images/logo.png', url='https://dmkpress.com/')
        db.session.add(new_shop)
        db.session.commit()
    else:
        new_shop = Shop.query.filter_by(name='ДМК Пресс').first()

    for book in books_list:
        edition_exists = Edition.query.filter(Edition.ISBN == book['ISBN']).count()
        if not edition_exists:
            title = book['title']
            year_of_edition = book['year_of_edition']
            ISBN = book['ISBN']
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
            new_edition = Edition.query.filter_by(ISBN=book['ISBN']).first()

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
