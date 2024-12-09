from flask import  render_template, flash, redirect, url_for, request, abort
from application.forms import RegistrationForm, LoginForm, PostForm, UpdateAccountForm
from application.models import User , Announcement
from application import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets, os, time


@app.route('/')
@app.route('/home')
def home():
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
     
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Welcome {form.username.data}')
            return redirect(url_for('home'))
        else:
            flash('log failed! Check username and password')
    return render_template('log_in.html', title='Log in page', form=form)

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Thankyou for {form.username.data} joining us .')
        return redirect(url_for('login'))
    return render_template('signUp.html', title='Sign up page', form=form)

@app.route('/aboutus')
def about_us():
    return render_template('aboutUs.html', title='About us page')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/announcements')
# @login_required
def announcements():
    posts=Announcement.query.all()
    return render_template('announcements.html', title='Announcements page', posts=posts)

## save picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    os.makedirs(os.path.join(app.root_path, 'static/profile_pics'), exist_ok=True)  # Ensure directory exists
    if not form_picture.filename:
        raise ValueError("Uploaded file has no filename.")
    form_picture.save(picture_path)
    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required 
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        # Handle profile picture update
        if form.profile.data:
            picture_file = save_picture(form.profile.data)
            current_user.img_file = picture_file  # Update user's image file
            print(f"Picture file saved as: {picture_file}")  # Debug
            
        # Update other user details
        current_user.email = form.email.data
        current_user.username = form.username.data

        try:
            db.session.commit()  # Commit all changes
            db.session.refresh(current_user)  # Ensure changes are reflected
            print(f"Updated image file: {current_user.img_file}")  # Debug
        except Exception as e:
            print(f"Database commit failed: {e}")
        
        # Redirect to avoid form resubmission
        return redirect(url_for('account'))

    elif request.method == 'GET':
        # Populate the form with current user data
        form.email.data = current_user.email
        form.username.data = current_user.username
        print(f"Loaded form: email={form.email.data}, username={form.username.data}")

    # Cache-busting for profile picture
    img_file = url_for('static', filename=f'profile_pics/{current_user.img_file}') + '?t=' + str(int(time.time()))
    print(f"Image file URL sent to template: {img_file}")

    return render_template('account.html', title='Account Page', img_file=img_file, form=form)
@app.route('/post/new', methods=['GET', 'POST'])
@login_required  
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Announcement(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'announced')
        return redirect(url_for('announcements'))

    return render_template('create_post.html', title='New Post', form=form, h3='Create Post')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    post = Announcement.query.get_or_404(post_id)
    return render_template('post.html', title='announcement', post=post)

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Announcement.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title =form.title.data
        post.content =form.content.data
        db.session.commit()
        flash('Announcement updated.')
        return redirect(url_for('announcements'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html', title='update announcement', post=post, form=form)

@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Announcement.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(f'Deleted')
    return redirect(url_for('announcements'))