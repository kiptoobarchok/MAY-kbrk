from application import db, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))



# database model users
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default='default.png')
    posts = db.relationship('Announcement', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', {self.img_file})"
    
class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"post [{self.title}, {self.date_posted}]"

