import redis
from flask import Flask, request, render_template, session, make_response, url_for
from flask_script import Manager
from flask_session import Session

app = Flask(__name__)


@app.route('/index/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/index/about.html/', methods=['GET', 'POST'])
def about():
    return render_template('about.html')


@app.route('/index/gbook/', methods=['GET'])
def gbook():
    return render_template('gbook.html')


@app.route('/index/info/', methods=['GET'])
def info():
    return render_template('info.html')


@app.route('/index/life/', methods=['GET'])
def life():
    return render_template('life.html')


@app.route('/index/list/', methods=['GET'])
def index_list():
    return render_template('list,html')


@app.route('/index/share/', methods=['GET'])
def share():
    return render_template('share.html')


@app.route('/index/time/', methods=['GET'])
def index_time():
    return render_template('time.html')


if __name__ == '__main__':
    manage = Manager(app)
    manage.run()
