from flask import Blueprint, request, render_template, redirect, session

from . import db
from .models import User

auth = Blueprint("auth", __name__)



@auth.route('/')
def home():
    if session.get('email'):
        return redirect('/dashboard')
    else:
        return render_template('login.html')



@auth.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')



@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')
    return render_template('login.html')



@auth.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')
