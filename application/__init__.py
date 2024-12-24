from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
import os

#load environment variables
load_dotenv()

app = Flask(__name__, static_url_path='/static')
secret_key=os.getenv('SECRET_KEY')
app.config['SECRET_KEY'] = secret_key

print(type(secret_key), secret_key)
if not secret_key:
    raise ValueError('SECRET_KEY environment variable is not set')


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///may_kbrk.db'

# Flask mail configuration
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS']=  os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail=Mail(app)

db = SQLAlchemy(app)
bcrypt =  Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

print(type(app.config['SECRET_KEY']), app.config['SECRET_KEY'])

from application import routes