import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from web.views import blue_web
from back.views import blue_back
from back.models import db

app = Flask(__name__)

app.register_blueprint(blueprint=blue_web, url_prefix='/web')
app.register_blueprint(blueprint=blue_back, url_prefix='/back')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/myblog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = 'sldfijie2983r9102304hvsdmvao3ir0u9'

app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

Session(app)
db.init_app(app)

manage = Manager(app)

if __name__ == '__main__':
    manage.run()
