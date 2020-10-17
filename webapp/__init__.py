from flask import current_app, Flask, render_template, url_for

from webapp.small_model import db, Edition

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
        title = 'Здесь надо показывать сведения из чертовой базы'
        books_list = Edition.query.all()
        return render_template('index.html', title=title, books_list=books_list)

    @app.route('/authors')
    def authors():
        title = 'Здесь будут сведения об авторе'
        return render_template('base.html', title=title)

    return app