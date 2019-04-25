from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class Category(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cat_name = db.Column(db.String(30), unique=True, nullable=False)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    __tablename__ = 'category'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Article(db.Model):
    art_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_title = db.Column(db.String(50), unique=True, nullable=False)
    tag = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.date.today())
    content = db.Column(db.Text, nullable=False)
    art_category = db.Column(db.Integer, db.ForeignKey('category.cat_id'), nullable=False)

    __tablename__ = 'article'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()