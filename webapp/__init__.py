from flask import Flask, render_template, request

from webapp.small_model import db, Edition, Author


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    @app.route('/')
    def index():
        books_list = Edition.query.all()
        authors_list = Author.query.all()
        return render_template('index.html',
                               books_list=books_list,
                               authors_list=authors_list)

    @app.route('/book/<book_id>')
    def book(book_id):
        book_info = Edition.query.get(book_id)
        publishing = book_info.publishing
        title = 'Скоро здесь будет книжка'
        return render_template('book.html', title=title, book_info=book_info,
                               publishing=publishing)

    @app.route('/author/<author_id>')
    def author(author_id):
        title = 'Здесь будут сведения об авторе'
        return render_template('base.html', title=title)

    @app.route('/publishing/<publishing_id>')
    def publishing(publishing_id):
        title = 'Здесь будут сведения об издательстве'
        return render_template('base.html', title=title)

    @app.route('/search/')
    def search():
        print(request.args)
        user_info = request.args.get('q')
        page = Edition.query.filter(Edition.title.like(f'%{user_info}%'))
        return render_template('index.html', books_list=page)


    return app
