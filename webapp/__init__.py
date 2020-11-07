from flask import Flask, render_template, request

from webapp.small_model import db, Edition, Author, Publishing, Catalog, Shop


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    # Файл html - в папке templates, название см. в render_template.
    # На странице должны быть карточки книг с названием, авторами и обложкой.
    # Имена авторов и названия книг - ссылки, которые ведут на индивидуальные страницы.
    # (реализовано максимально некрасиво)
    # Желательно сделать постраничную выдачу, чтобы вся база сразу не вываливалась.

    def index():
        books_list = Edition.query.all()
        authors_list = Author.query.all()
        return render_template('index.html',
                               books_list=books_list,
                               authors_list=authors_list)

    @app.route('/book/<book_id>')
    # Здесь должны быть все сведения о книге, которые удалось получить:
    # Название (my_book.title / my_book)
    # Авторы (my_book.author_id - это список, надо к нему обращаться циклом)
    # Год издания (my_book.year_of_edition)
    # Издательство (my_book.my_publishing)
    # ISBN (my_book.ISBN)
    # Обложка (my_book.cover)
    # Аннотация (my_book.annotation)
    # Цена на наших двух площадках (нужно получать циклом из my_catalog по атрибуту price)
    # Страница, где продается книга (атрибут url элементов из my_catalog)
    # Названия магазинов, их логотипы (атрибуты name, logo). Название магазина можно также получить от класса Catalog по атрибуту my_shop
    def book(book_id):
        my_book = Edition.query.get(book_id)
        my_catalog = Catalog.query.filter(Catalog.book == book_id).all()
        shop_list = Shop.query.all()
        return render_template('book.html', my_book=my_book, my_catalog=my_catalog, shop_list=shop_list)

    @app.route('/author/<author_id>')
    # Про авторов у нас почти ничего не собрано. Должен выдаваться только список его книг.
    # Список лежит в my_author.editions, но там только названия.
    # Нужно зайти в books-list, отфильтровать нужную книгу по названию и использовать ее атрибуты для получения любой инфы.
    def author(author_id):
        my_author = Author.query.get(author_id)
        books_list = Edition.query.filter(Edition.author_id.any(id=author_id))
        return render_template('author.html', my_author=my_author,
                               books_list=books_list)

    @app.route('/search/')
    def search():
        print(request.args)
        user_info = request.args.get('q')
        page = Edition.query.filter(Edition.title.like(f'%{user_info}%'))
        return render_template('index.html', books_list=page)

    return app
