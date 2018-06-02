from redis import StrictRedis

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

class DevelopConfig(Config):

    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/economic_dev_news'

class ProductionConfig(Config):

    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/economic_pro_news'

class UnittestingConfig(Config):

    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/economic_test_news'

configs = {
    'dev': DevelopConfig,
    'pro': ProductionConfig,
    'unit': UnittestingConfig
}