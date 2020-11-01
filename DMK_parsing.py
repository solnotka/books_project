import requests
from bs4 import BeautifulSoup
from webapp.db import db
from webapp.small_model import Edition, Author, Publishing, Catalog, Shop

sitemap_url = requests.get('https://dmkpress.com/sitemap.xml')


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
        soup_html = BeautifulSoup(requests.get(res).text)
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
                authors = (info_list[i + 1]).replace('Дата выхода', ''). replace('Формат', '')
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
                        ISBN = (ISBN.replace(number, '')).strip()

        annotation_card = soup_html.find('div', class_='card-note')
        if annotation_card:
            annotation = str(annotation_card.text).replace('Аннотация', '')
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
        
        books_list.append(book)
    
    return books_list


def save_books(url):
    res_list = get_url_list(url)
    books_list = get_book_data(res_list)
    for book in books_list:
        

for book in books_list[:100]:
    print(book['res'])
    print(book['authors_list'])
    print(book['annotation'])
    print(book['cover'])
    print(book['price'])
