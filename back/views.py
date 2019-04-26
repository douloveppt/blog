import base64
import datetime
import math
import os

from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from back.models import User, Article, Category, db
from utils.faceid import register_face_user, match_face
from utils.functions import is_login
from utils.settings import IMAGE_DIR

blue_back = Blueprint('back', __name__)


@blue_back.route('/index/', methods=['GET', 'POST'])
@is_login
def index():
    user_id = session['user_id']
    username = User.query.filter(User.user_id == user_id).first().username
    arts_num = len(Article.query.filter().all())
    # print(arts_num)
    return render_template('back/index.html', username=username, arts_num=arts_num)


@blue_back.route('/category/', methods=['GET', 'POST'])
@is_login
def category():
    user_id = session['user_id']
    username = User.query.filter(User.user_id == user_id).first().username
    cates = Category.query.all()
    if request.method == 'GET':
        if not cates:
            return render_template('back/category.html', username=username)
        cates_num = len(Category.query.all())
        return render_template('back/category.html', cates=cates, username=username, cates_num=cates_num)
    if request.method == 'POST':
        cat_name = request.form.get('name')
        cat = Category()
        cat.cat_name = cat_name
        cat.save()
        return redirect(url_for('back.category'))


@blue_back.route('/article/', methods=['GET', 'POST'])
@is_login
def article():
    user_id = session['user_id']
    username = User.query.filter(User.user_id == user_id).first().username
    arts = Article.query.all()
    # cate = Category.query.all()
    if request.method == 'GET':
        if not arts:
            return render_template('back/article.html', username=username)
        art_num = len(Article.query.all())
        return render_template('back/article.html', arts=arts, username=username, Category=Category, art_num=art_num)


@blue_back.route('/add_article/', methods=['GET', 'POST'])
@is_login
def add_article():
    date = datetime.date.today()
    user_id = session['user_id']
    username = User.query.filter(User.user_id == user_id).first().username
    if request.method == 'GET':
        cates = Category.query.all()
        return render_template('back/add_article.html', cates=cates, username=username, date=date)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        # cat_name = request.form.get('category')
        tags = request.form.get('tags')
        category = request.form.get('category')
        # print(category)
        if title and content and category:
            user_id = session['user_id']
            username = User.query.filter(User.user_id == user_id).first().username
            article = Article()
            article.art_title = title
            article.content = content
            article.author = username
            article.tag = tags
            article.art_category = category
            article.save()
            return redirect(url_for('back.article'))
        return render_template('back/add_article.html', username=username, date=date)


@blue_back.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        face = request.form.get('face')
        if username and password and password2 and face:
            user = User.query.filter(User.username == username).first()
            if user:
                error = '该账号已被注册！'
                return render_template('back/register.html', error=error)
            else:
                img = face.split(',')[-1]
                if not register_face_user(img, username):
                    error = '注册失败'
                    return render_template('back/register.html', error=error)
                if password2 == password:
                    file = base64.b64decode(img)
                    img_dir = os.path.join(IMAGE_DIR, username + '.jpg')
                    with open(img_dir, 'wb') as f:
                        f.write(file)
                    user = User()
                    user.username = username
                    user.password = generate_password_hash(password)
                    user.save()
                    return redirect(url_for('back.login'))
                else:
                    error = '两次密码不一致'
                    return render_template('back/register.html', error=error)
        else:
            error = '信息不完整！'
            return render_template('back/register.html', error=error)


@blue_back.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请先注册！'
                return render_template('back/login.html', error=error)
            if not check_password_hash(user.password, password):
                error = '密码错误！请重新输入！'
                return render_template('back/login.html', error=error)
            session['user_id'] = user.user_id
            return redirect(url_for('back.index'))
        else:
            error = '请填写完整的登录信息！'
            return render_template('back/login.html', error=error)


@blue_back.route('/face_login/', methods=['GET', 'POST'])
def face_login():
    if request.method == 'GET':
        return render_template('back/face_login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        face = request.form.get('face')
        if username and face:
            user = User.query.filter(User.username == username).first()
            if not user:
                error = '该账号不存在，请先注册！'
                return render_template('back/login.html', error=error)
            img = face.split(',')[-1]
            file = os.path.join(IMAGE_DIR, username + '.jpg')
            file_exists = os.path.exists(file)
            if not file_exists:
                return render_template('back/login.html', error='该账号没有保存的人脸信息')
            score = match_face(img, file)
            if score < 80:
                return render_template('back/login.html', error='匹配不成功')
            session['user_id'] = user.user_id
            return redirect(url_for('back.index'))
        else:
            return render_template('back/face_login.html', error='登录失败，请重新登录！')


@blue_back.route('/logout/', methods=['GET'])
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))


@blue_back.route('/del_art/', methods=['GET', 'POST'])
def del_art():
    if request.method == 'POST':
        id = request.get_data('id').decode('utf-8')[3:]
        # print(id)
        art = Article.query.get(id)
        db.session.delete(art)
        db.session.commit()
        return jsonify({'code': '200', 'msg': '删除成功！'})


@blue_back.route('/del_cate/', methods=['GET', 'POST'])
def del_cate():
    if request.method == 'POST':
        id = request.get_data('id').decode('utf-8')[3:]
        # print(id)
        cate = Category.query.get(id)
        arts = Article.query.filter(Article.art_category == cate.cat_id).all()
        for art in arts:
            art.delete()
        cate.delete()
        return jsonify({'code': '200', 'msg': '操作成功'})


@blue_back.route('/search/<string:keywords>/', methods=['GET', 'POST'])
def search(keywords):
    arts = Article.query.all()
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass


@blue_back.route('/modify/<int:id>/', methods=['GET', 'POST'])
def modify(id):
    art = Article.query.filter(Article.art_id == id).first()
    user_id = session['user_id']
    username = User.query.filter(User.user_id == user_id).first().username
    title = art.art_title
    content = art.content
    date = datetime.date.today()
    cate = art.category.cat_name
    if request.method == 'GET':
        cates = Category.query.all()
        return render_template('back/mod_article.html', cates=cates, username=username, title=title, content=content,
                               date=date, cate=cate)
    if request.method == 'POST':
        title2 = request.form.get('title')
        content2 = request.form.get('content')
        tags2 = request.form.get('tags')
        category2 = request.form.get('category')
        # print(category)
        if title and content and category:
            # article = Article()
            # article.art_id = id
            art.art_title = title2
            art.content = content2
            art.author = username
            art.tag = tags2
            art.art_category = category2
            # article.save()
            db.session.commit()
            return redirect(url_for('back.article'))


@blue_back.route('/get_page/', methods=['GET', 'POST'])
def get_page():
    if request.method == 'POST':
        all_arts = []
        arts = Article.query.all()
        # total = len(arts)
        # page_size = 5
        # total_page = math.ceil(total / page_size)
        # json = {'total': total, 'page_size': page_size, 'total_page': total_page}
        for art in arts:
            all_arts.append(art.art_title)
        json = {'art': all_arts}
        return jsonify(json)
