from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

app = Flask(__name__)
app.debug = True

secret_key = os.getenv('MIMICTF_SECRET_KEY')
app.config['SECRET_KEY'] = f'{secret_key}'

db_user = os.getenv('MYSQL_MIMICTF_DB_USER')
db_password = os.getenv('MYSQL_MIMICTF_DB_USER_PASSWORD')
db_host = os.getenv('MYSQL_MIMICTF_DB_HOST')
db_name = os.getenv('MYSQL_MIMICTF_DB_NAME')
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = ''

from views import *

if __name__ == "__main__":
    app.run()