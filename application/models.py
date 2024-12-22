from application import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):   
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=1)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20),  nullable=False)
    email = db.Column(db.String(120), unique=1, nullable=0)
    username = db.Column(db.String(20), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False, default='member')
    branch = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Announcement', backref='author', lazy=True)

    def __repr__(self):
        return f"{self.image_file} - {self.firstname} {self.lastname}, {self.branch}-[{self.role}]"

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    scripture_reading = db.Column(db.Text, nullable=False)
    memory_verse = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    introduction = db.Column(db.Text)
    conclusion = db.Column(db.Text)
    body = db.relationship('Body', backref='Lesson.id', lazy="joined")

    def __repr__(self):
        return f"Lesson {self.id}:  {self.title}"
    
class Body(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text)
    answers = db.Column(db.Text)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=0)

    def __repr__(self):
        return f"Q&A:  {self.question}, {self.answers} - Lesson {self.lesson_id}"