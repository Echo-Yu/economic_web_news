from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/economic_news'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    SECRET_KEY = 'ASDFASDFASFDASDF'
    SESSION_TYPE = 'redis'
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USE_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 3600 * 24


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
Migrate(app, db)
redis_store = StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)
CSRFProtect(app)
Session(app)

@app.route('/')
def index():
    # from flask import session
    # session['age']='2'
    return 'Hello World!'

if __name__ == '__main__':
    manager.run()
