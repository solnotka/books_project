#Временная модель для запуска
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Edition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    publishing = db.Column(db.String)
    edition_number = db.Column(db.Integer)
    ISBN = db.Column(db.String, unique=True, nullable=False)   
    cover = db.Column(db.String)

    def __repr__(self):
        return f'{self.title}'

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudonim = db.Column(db.String, unique=True, nullable=False)
    real_name = db.Column(db.String, nullable=False)
    photo = db.Column(db.String)
    editions = db.relationship('Edition', lazy='joined', backref='my_author')

    def __repr__(self):
        return f'{self.pseudonim}'