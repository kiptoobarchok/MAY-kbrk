from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager 

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '392ed6116bcd27c6ac099518ca51c150'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///may_kbrk.db'

db = SQLAlchemy(app)
bcrypt =  Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from application import routes