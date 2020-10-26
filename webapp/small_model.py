# Временная модель для запуска

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

authors = db.Table('authors',
                    db.Column('edition_id', db.ForeignKey('edition.id'),
                              primary_key=True),
                    db.Column('author_id', db.ForeignKey('author.id'),
                              primary_key=True))


class Edition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.relationship('Author', secondary=authors, lazy='subquery', backref=db.backref('my_editions', lazy=True))
    edition_number = db.Column(db.Integer)
    year_of_edition = db.Column(db.DateTime, nullable=True)
    publishing = db.Column(db.Integer, db.ForeignKey('publishing.id'), nullable=False)
    ISBN = db.Column(db.String, unique=True, nullable=False)
    cover = db.Column(db.String)
    annotation = db.Column(db.Text)
    items = db.relationship('Catalog', backref='my_edition')

    def __repr__(self):
        return f'{self.title}'


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudonim = db.Column(db.String, unique=True, nullable=False)
    real_name = db.Column(db.String, nullable=False)
    photo = db.Column(db.String)
    editions = db.relationship('Edition', secondary=authors, lazy='subquery',
                               backref=db.backref('my_authors', lazy=True))

    def __repr__(self):
        return f'{self.pseudonim}'


class Publishing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    logo = db.Column(db.String)
    books = db.relationship('Edition', backref='my_publishing')
    town = db.Column(db.String)
    url = db.Column(db.String, unique=True)
    adress = db.Column(db.String)

    def __repr__(self):
        return f'{self.name}'


class Catalog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String, db.ForeignKey('edition.id'), nullable=False)
    point_of_sell = db.Column(db.String, db.ForeignKey('shop.id'),
                              nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Catalog: {self.book}, {self.point_of_sell}>'


class Shop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    adress = db.Column(db.String)
    items = db.relationship('Catalog', backref='my_shop')

    def __repr__(self):
        return f'{self.name}>'
