
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
# from info import app, db
from info import create_app

app = create_app('dev')
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# Migrate(app, db)

@app.route('/')
def index():
    # from flask import session
    # session['age']='2'
    return 'Hello World!'


if __name__ == '__main__':
    manager.run()
