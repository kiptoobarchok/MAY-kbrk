from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv
from flask_migrate import Migrate
import os

#load environment variables 
load_dotenv()

app = Flask (__name__, static_url_path='/static')
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
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

print(type(app.config['SECRET_KEY']), app.config['SECRET_KEY'])

from application.users.routes import users
from application.main.routes import main
from application.lessons.routes import lessons_bp
from application.events.routes import events_bp
from application.announcements.routes import announcements_bp


app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(lessons_bp)
app.register_blueprint(events_bp)
app.register_blueprint(announcements_bp)
 