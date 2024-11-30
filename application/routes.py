from flask import  render_template, flash, redirect, url_for
from application.forms import RegistrationForm, LoginForm
from application.models import User , Post
from application import app

posts = [
    {
    'author': {'username': 'pastor Eliud'},
    'body': 'attend wednesday church at Edmond\'s!',
    'date_posted': 'Nov 26th , 2024',
    'profile_pic': '!picture1.img'
    },
    {
    'author': {'username': 'Josphat'},
    'body': 'remember to give tithes...',
    'date_posted': 'Nov 18th , 2024',
    'profile_pic': '!picture2.img'
    },
    {
    'author': {'username': 'purity'},
    'body': 'church harambee next saturday',
    'date_posted': 'Nov 28th , 2024',
    'profile_pic': '!picture3.img'
    },
    {
    'author': {'username': 'john doe'},
    'body': 'youths yearly congregation',
    'date_posted': 'Nov 28th , 2024',
    'profile_pic': '!picture4.img'
    },
    {
    'author': {'username': 'jane doe'},
    'body': 'kanisa ya wamama',
    'date_posted': 'Nov 28th , 2024',
    'profile_pic': '!picture5.img'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'caleb9090' and form.password.data == 'admin':
            flash(f'logged in as {form.username.data}')
            return redirect(url_for('home'))
        else:
            flash(f'log in failed!\nCheck your password and username correctly.')
    return render_template('log_in.html', title='Log in page', form=form)

@app.route('/signup', methods=['GET', 'POST']) 
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'account created for {form.username.data} successfully.')
        return redirect(url_for('home'))
    return render_template('signUp.html', title='Sign up page', form=form)

@app.route('/aboutus')
def about_us():
    return render_template('aboutUs.html', title='About us page')

@app.route('/announcements')
def announcements():
    return render_template('announcements.html', title='Announcements page', posts=posts)
