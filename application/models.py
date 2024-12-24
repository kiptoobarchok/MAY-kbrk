from application import db, login_manager, app
from flask_login import UserMixin
from datetime import datetime
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer


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
    date_of_birth = db.Column(db.Date, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Announcement', backref='author', lazy=True)

    def generate_reset_token(self, expires_sec=1800):
        print("DEBUG KEY TYPE:", type(app.config['SECRET_KEY']), app.config['SECRET_KEY'])
        secret_key = app.config['SECRET_KEY']
        serializer = URLSafeTimedSerializer(secret_key)

        return serializer.dumps({'user_id': self.id})
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


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