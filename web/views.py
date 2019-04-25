from flask import Blueprint, request, render_template, redirect, url_for

from back.models import Article, Category

blue_web = Blueprint('web', __name__)


@blue_web.route('/index/', methods=['GET', 'POST'])
def index():
    cates = Category.query.all()
    if request.method == 'GET':
        arts = Article.query.all()

        return render_template('web/index.html', arts=arts, cates=cates)


@blue_web.route('/about/', methods=['GET', 'POST'])
def about():
    cates = Category.query.all()
    return render_template('web/about.html', cates=cates)


@blue_web.route('/art_details/<int:id>/', methods=['GET'])
def art_details(id):
    cates = Category.query.all()
    art = Article.query.filter(Article.art_id == id).first()
    title = art.art_title
    content = art.content
    author = art.author
    return render_template('web/art_details.html', title=title, content=content, author=author, cates=cates)


@blue_web.route('/category/<int:id>/', methods=['GET'])
def category(id):
    cates = Category.query.all()
    if request.method == 'GET':
        arts = Article.query.filter(Article.art_category == id).all()
        return render_template('web/category.html', arts=arts, cates=cates)
