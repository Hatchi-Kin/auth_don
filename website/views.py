import time
from flask import Blueprint, request, render_template, redirect, session, url_for

from .ics_cal import MyIcs
from .hug_api import Narrator
from . import db
from .models import User, Post, HugPost, BadWords
from .data import Data


views = Blueprint("views", __name__)



@views.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        random_bad = BadWords.get_random_bad_word()
        bad_word = random_bad[0]
        definition = random_bad[1]
        return render_template('dashboard.html',user=user, bad_word=bad_word, definition=definition)
    return redirect('/login')



@views.route('/le_pardon')
def le_pardon():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('le_pardon.html', user=user)
    return redirect('/login')



@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        if request.method == 'POST':
            if request.form['name'] == '':
                username = user.name
            else:
                username = request.form['name']
            text = request.form['message']
            new_post = Post(username=username,text=text)
            db.session.add(new_post)
            db.session.commit()
        msg_count = Post.query.count()
        last_ten = Post.get_last_ten_posts()
        return render_template('contact.html', last_ten=last_ten ,msg_count=msg_count, user=user)
    return redirect('/login')



@views.route('/hug_chat', methods=['GET', 'POST'])
def hug_chat():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        if request.method == 'POST':
            username = user.name
            text = request.form['message']
            new_post = HugPost(is_human=True,username=username,text=text)
            db.session.add(new_post)
            db.session.commit()
            narrator = Narrator()
            hug = narrator.get_hugging_answer(text)
            new_hug = HugPost(is_human=False,username="HugBot",text=hug)
            db.session.add(new_hug)
            db.session.commit()
        last_ten = HugPost.get_last_ten_hugs()
        return render_template('hug_chat.html', last_ten=last_ten , user=user)
    return redirect('/login')



@views.route('/room_ba', methods=['GET', 'POST'])
def room_ba():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        event_matin = MyIcs()
        event_matin.set_all_myics("matin")
        event_aprem = MyIcs()
        event_aprem.set_all_myics("aprem")
        event_demain = MyIcs()
        event_demain.set_all_myics("demain")
        return render_template('room_ba.html', event_matin=event_matin, event_aprem=event_aprem, event_demain=event_demain, user=user)
    return redirect('/login')


@views.route('/promesse_don', methods=['GET', 'POST'])
def promesse_don():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        rankings = Data.get_top_ten()
        rankings = rankings[:10]
        total_pledges = Data.get_total_pledges()
        if request.method == 'POST':
            pledge = request.form['pledges_euro']
            name = request.form['name']
            last_name = request.form['last_name']
            email = request.form['email']
            Data.save_entry(name, last_name, email, pledge)
            # Redirect to the same page with a query parameter that changes on each request
            return redirect(url_for('views.promesse_don', _anchor='pledge-form', _cache_buster=int(time.time())))
        
        rankings = Data.get_top_ten()
        rankings = rankings[:10]
        total_pledges = Data.get_total_pledges()
        return render_template('/promesse_don.html', user=user, rankings=rankings, total_pledges=total_pledges)
    
    return redirect('/login')



