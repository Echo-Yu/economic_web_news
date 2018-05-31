from flask import Flask

app = Flask(__name__)

class Config(object):
    DEBUG = True

app.config.from_object(Config)

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
