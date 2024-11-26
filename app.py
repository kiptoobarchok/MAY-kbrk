#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect


app = Flask(__name__)


# My Dummy data
user = {'username': 'KIPTOO'}

# data base call
posts = [
    {
    'author': {'username': 'pastor Eliud'},
    'body': 'attend wednesday church at Edmond\'s!',
    'date_posted': 'Nov 26th , 2024'
    },
    {
    'author': {'username': 'Josphat'},
    'body': 'remember to give tithes...',
    'date_posted': 'Nov 18th , 2024'
    },
    {
    'author': {'username': 'purity'},
    'body': 'church harambee next saturday',
    'date_posted': 'Nov 28th , 2024'
    }
]

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home_page.html')


@app.route('/login', methods=['GET', 'POST'])
def log_in():
    return render_template('log_in.html')

@app.route('/signup')
def sign_up():
    return render_template('signUp.html')

@app.route('/aboutus')
def about_us():
    return render_template('aboutUs.html')

@app.route('/announcements')
def announcements():
    return render_template('announcements.html', posts=posts, user=user)

if __name__ == '__main__':
    app.run(debug=1, port=5555)