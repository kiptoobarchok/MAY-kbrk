from flask import Blueprint
from application import db, bcrypt
from flask import render_template, url_for, redirect, flash, request
from application.main.forms import (LoginForm, SignupForm)
from application.models import User
from flask_login import current_user, login_user, login_required, logout_user


main = Blueprint('main', __name__)

@main.route('/')
def home():  
  return render_template('home.html', title='Home')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
  if  current_user.is_authenticated:
     return redirect(url_for('main.home'))
  form = SignupForm() 
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, username=form.username.data, role=form.role.data, branch=form.branch.data, date_of_birth=form.date_of_birth.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('main.login'))
  return render_template('signup.html', title='Sign Up', form=form)

# log in function
@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
     
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('log failed! Check email and password')
    return render_template('login.html', title='Log in', form=form)
@main.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('main.home'))


@main.route('/about_us')
def about_us():
    return render_template('about_us.html', title='About Us')

@main.route('/members', methods=['GET'])
@login_required  
def members():
  page  = request.args.get('page', 1, type=int)
  members = User.query.order_by(User.username.asc()).paginate(page=page, per_page=25)
  return render_template('members.html', title='Member\'s', members=members)

@main.route('/members/pastor', methods=['GET'])
@login_required  
def Pastor():
  pastor = User.query.filter_by(role='pastor').first()
  # if p.branch == 'kaborok':
  #   p = _pstr
  # pastor = p
  return render_template('pastor.html', title='Pastor\'s', pastor=pastor)
