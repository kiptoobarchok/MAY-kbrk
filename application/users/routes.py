from flask import Blueprint
from application import db, bcrypt, mail, app
from flask import render_template, url_for, redirect, flash, request
from application.users.forms import (UpdateAccountForm, ResetPasswordForm, RequestResetForm)
from application.models import User,Announcement
from flask_login import current_user,  login_required
from flask_mail import Message
from flask import current_app
import secrets, os, time
from PIL import Image


users = Blueprint('users', __name__ )

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
  if old_picture != 'default.jpg':
    old_picture_path = os.path.join(current_app.root_path, 'static/profile_pics', old_picture)
    if os.path.exists(old_picture_path):
      os.remove(old_picture_path)

  return picture_fn


@users.route('/account', methods=['GET', 'POST'])
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
      return redirect(url_for('users.account'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    form.firstname.data = current_user.firstname
    form.lastname.data = current_user.lastname

  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  return render_template('account.html', title='Account', form=form, image_file=image_file, announcements=announcements)


def send_reset_email(user):
  token = user.generate_reset_token()
  msg = Message('Password Reset Request', sender='kiptoobarchok8032@gmail.com',
                recipients=[user.email])
  msg.body=f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request simply ignore this email and no change will be made
'''
  mail.send(msg)



@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
  form = RequestResetForm()
  if  current_user.is_authenticated:
    return redirect(url_for('main.home'))
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first_or_404()
    send_reset_email(user)
    flash('an email with instructions to reset your password has been sent to your email')
  return render_template   ('reset_request.html', title='Request Reset Token', form=form)

@users.route ('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
  if  current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  user = User.verify_reset_token(token)
  if not user:
    flash('Invalid or exprired token')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user.password = hashed_password
    db.session.commit()
    return redirect(url_for('main.login'))
  return render_template('reset_token.html', title='Request Reset Token', form=form)

 