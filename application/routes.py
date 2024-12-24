from application import app, db, bcrypt, mail
from flask import render_template, url_for, redirect, flash, request, abort
from application.forms import (LoginForm, SignupForm, UpdateAccountForm,
                              CreateAnnouncementForm,UpdateAnnouncementForm ,
                              AddLessonForm, AddBodyForm,ResetPasswordForm, RequestResetForm)
from application.models import User,Announcement, Lesson, Body
from flask_login import current_user, login_user, login_required, logout_user
import secrets, os, time
from PIL import Image
from flask import current_app
from flask_mail import Message


@app.route('/')
def home():  
  return render_template('home.html', title='Home')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if  current_user.is_authenticated:
     return redirect(url_for('home'))
  form = SignupForm() 
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data, username=form.username.data, role=form.role.data, branch=form.branch.data, date_of_birth=form.date_of_birth.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('signup.html', title='Sign Up', form=form)

# log in function
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('log failed! Check email and password')
    return render_template('login.html', title='Log in', form=form)
@app.route('/logout')
def logout():
   logout_user()
   return redirect(url_for('home'))

## Role based Access
# def role_required(role):
#   def decorator(func):
#     def wrapper(*args, **kwargs):
#       if current_user.role != role:
#         abort(403)
#       return func(*args, **kwargs)
#     return wrapper
#   return decorator
      


# function to save the picture
def save_picture(form_picture, old_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn =random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  output_size = (125, 125)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)

## delete old picture from the db if its not default
  if old_picture != 'default.png':
    old_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', old_picture)
    if os.path.exists(old_picture_path):
      os.remove(old_picture_path)

  return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  announcements = Announcement.query.filter_by(user_id=current_user.id)
  if form.validate_on_submit():
    if form.profile.data:
      old_picture = current_user.image_file
      picture_file = save_picture(form.profile.data, old_picture)
      current_user.image_file = picture_file
      db.session.add(current_user)  # Explicitly add current_user to the session
    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.firstname = form.firstname.data
    current_user.lastname = form.lastname.data
    try:
      db.session.commit()
      db.session.refresh(current_user)  # Ensure current_user reflects latest data
      print(f"Updated image file: {current_user.image_file}")  # Debug
    except Exception as e:
      print(f"Database commit failed: {e}")
      return redirect(url_for('account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname

  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', form=form, image_file=image_file, announcements=announcements)


@app.route('/about_us')
def about_us():
    return render_template('about_us.html', title='About Us')


## Announcements
@app.route('/announcements')
def announcements():
  # create for every branch (*args, **kwargs)
  if not (current_user.is_authenticated):
    abort(403)
  if current_user.branch != 'kaborok':
    abort(403)

  page = request.args.get('page', 1, type=int)
  announcements=Announcement.query.order_by(Announcement.date_posted.desc()).paginate(page=page, per_page=15)
  return render_template('announcements.html', title='Announcement', announcements=announcements)


@app.route('/announcement/new ', methods=['GET', 'POST'])
@login_required
def create_announcement():
  form = CreateAnnouncementForm()
  if form.validate_on_submit():
    announcement =Announcement(title=form.title.data, content=form.content.data, author=current_user)
    db.session.add(announcement)
    db.session.commit()
    print('Added to the db')
    return redirect(url_for('announcements'))
  else:
    print("failed to add announcement")
  return render_template('create_announcement.html', title='New Announcement' , form=form)

@app.route('/announcement/<int:announcement_id> ', methods=['GET', 'POST'])
@login_required
def show_announcement(announcement_id):
   announcement = Announcement.query.get_or_404(announcement_id)
   return render_template('show_announcement.html', title='Announcement', announcement=announcement)


@app.route('/announcement/<int:announcement_id>/update ', methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
  announcement = Announcement.query.get_or_404(announcement_id)
  form = UpdateAnnouncementForm()
  if announcement.author != current_user:
     abort(403)

  if form.validate_on_submit():
    announcement.title = form.title.data
    announcement.content = form.content.data
    db.session.commit()
    db.session.refresh(announcement)
    print('update successful')
    return redirect(url_for('show_announcement', announcement_id=announcement.id))
  elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
        
  return render_template('create_announcement.html', title='Update nnouncement', form=form, announcement=announcement)

@app.route('/announcement/<int:announcement_id>/delete ', methods=['GET', 'POST'])
@login_required
def delete_announcement(announcement_id):
  announcement = Announcement.query.get_or_404(announcement_id)
  if announcement.author != current_user:
    abort(403)

  db.session.delete(announcement)
  db.session.commit()
  print(f'Deleted')
  return redirect(url_for('announcements'))


## Lessons
@app.route('/lessons', methods=['GET'])
@login_required
def lessons():
    page = request.args.get('page', 1, type=int)
    lessons = Lesson.query.order_by(Lesson.date_posted.desc()).paginate(page=page, per_page=10)
    print(type(lessons))  # Check the type of `lessons`
    return render_template('lessons.html', title='Sabbath Lessons', lessons=lessons)


@app.route('/add_lesson', methods=['GET', 'POST'])
@login_required
def add_lesson():
    if current_user.role != 'admin':
      abort(403)
    form = AddLessonForm()
    if form.validate_on_submit():
        lesson = Lesson(title=form.title.data,date_posted=form.date_posted.data, scripture_reading=form.scripture_reading.data, memory_verse=form.memory_verse.data, introduction=form.introduction.data, conclusion=form.conclusion.data)
        db.session.add(lesson)
        db.session.commit()
        print('lesson added...')
        return redirect(url_for('lessons'))
    print('failed to add')
    return render_template('add_lesson.html', title='Add Lesson' , form=form)

@app.route('/lesson/<int:lesson_id>', methods=['GET'])
@login_required  
def view_lesson(lesson_id):
    # Fetch the lesson from the database by its ID
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('view_lesson.html', title=lesson.title, lesson=lesson)

## update lesson

@app.route('/lesson/<int:lesson_id>/update', methods=['GET', 'POST'])
@login_required  
def update_lesson(lesson_id):
    if current_user.role != 'admin':
      abort(403)
    # Fetch the lesson from the database by its ID
    lesson = Lesson.query.get_or_404(lesson_id)
    form = AddLessonForm()
    if form.validate_on_submit():
        lesson.title = form.title.data
        lesson.date_posted = form.date_posted.data
        lesson.scripture_reading = form.scripture_reading.data
        lesson.memory_verse = form.memory_verse.data
        lesson.introduction = form.introduction.data
        lesson.conclusion = form.conclusion.data
        db.session.commit()
        db.session.refresh(lesson)
        print('update successful')
        return redirect(url_for('lessons', lesson_id=lesson.id))
    elif request.method == 'GET':
        form.title.data = lesson.title
        form.date_posted.data = lesson.date_posted 
        form.scripture_reading.data = lesson.scripture_reading
        form.memory_verse.data = lesson.memory_verse
        form.introduction.data = lesson.introduction
        form.conclusion.data = lesson.conclusion
    return render_template('update_lesson.html', title=lesson.title, lesson=lesson, form=form)

@app.route('/add_content', methods=['GET', 'POST'])
@login_required  
def add_content():
    if current_user.role != 'admin':
      abort(403)
    form =AddBodyForm()
    if form.validate_on_submit():
        body = Body(question=form.question.data, answers=form.answers.data, lesson_id=form.lesson_id.data)
        db.session.add(body)
        db.session.commit()
        return redirect(url_for('lessons'))
    print('unsuccessful')
    return render_template('add_content.html', title='Add Q and A', form=form)

@app.route('/lesson/<int:lesson_id>/body', methods=['GET'])
@login_required  
def view_body(lesson_id):
    body = Body.query.filter_by(lesson_id=lesson_id).all()
    return render_template('view_body.html', title='Question and Answers' , body=body)


## update question and answers
@app.route('/lesson/<int:lesson_id>/body/<int:body_id>', methods=['GET', 'POST'])
@login_required  
def update_body(lesson_id, body_id):
    body = Body.query.filter_by(lesson_id).first(body_id)
    form = AddBodyForm()
    if form.validate_on_submit():
        body.question = form.question.data
        body.answers = form.answers.data
        body.lesson_id = form.lesson_id.data
        db.session.commit()
        db.session.refresh(body)
        return redirect(url_for('view_body', lesson_id=body.lesson_id))
    elif request.method == 'GET':
        form.question.data = body.question
        form.answers.data = body.answers
        form.lesson_id.data = body.lesson_id 
    return render_template('update_body.html', title='Update Questions and Answers', body=body, form=form)


@app.route('/lesson/<int:lesson_id>/delete ', methods=['GET', 'POST'])
@login_required
def delete_lesson(lesson_id):
  lesson = Lesson.query.get_or_404(lesson_id)
  if current_user.role != 'admin':
    abort(403)

  db.session.delete(lesson)
  db.session.commit()
  print('lesson deleted...')
  return redirect(url_for('lessons'))


@app.route('/members', methods=['GET'])
@login_required  
def members():
  page  = request.args.get('page', 1, type=int)
  members = User.query.order_by(User.username.asc()).paginate(page=page, per_page=25)
  return render_template('members.html', title='Member\'s', members=members)

@app.route('/members/pastor', methods=['GET'])
@login_required  
def Pastor():
  pastor = User.query.filter_by(role='pastor').first()
  return render_template('pastor.html', title='Pastor\'s', pastor=pastor)

## should have's

@app.route('/announcements/schedule', methods=['GET'])
@login_required  
def sabbath_schedule():
  return render_template('sabbath_schedule.html', title='Sabbath Schedule')



def send_reset_email(user):
  token = user.generate_reset_token()
  msg = Message('Password Reset Request', sender='kiptoobarchok8032@gmail.com',
                recipients=[user.email])
  msg.body=f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request simply ignore this email and no change will be made
'''
  mail.send(msg)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
  form = RequestResetForm()
  if  current_user.is_authenticated:
    return redirect(url_for('home'))
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first_or_404()
    send_reset_email(user)
    flash('an email with instructions to reset your password has been sent to your email')
  return render_template('reset_request.html', title='Request Reset Token', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
  if  current_user.is_authenticated:
    return redirect(url_for('home'))
  
  user = User.verify_reset_token(token)
  if not user:
    flash('Invalid or exprired token')
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user.password = hashed_password
    db.session.commit()
    return redirect(url_for('login'))
  return render_template('reset_token.html', title='Request Reset Token', form=form)
