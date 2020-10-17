from flask import current_app, Flask, render_template, url_for

from webapp.small_model import db, Edition, Author

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Скоро здесь будет много книжек'
        return render_template('base.html', title=title)

    @app.route('/books')
    def books():
        title = 'Книги'
        books_list = Edition.query.all()
        authors_list = Author.query.all()
        return render_template('index.html', title=title, books_list=books_list, authors_list=authors_list)
    
    @app.route('/book/<book_id>')
    def book(book_id):
        book_info = Edition.query.get(book_id)
        publishing = book_info.publishing
        title = 'Скоро здесь будет книжка'
        return render_template('book.html', title=title, book_info=book_info, publishing=publishing)

    @app.route('/authors')
    def authors():
        title = 'Здесь будут сведения об авторе'
        return render_template('base.html', title=title)

    return app