from app import app
from flask import render_template, url_for, redirect, flash
from flask_login import login_required, login_user, current_user, logout_user
from forms import LoginForm, RegisterForm
from app import db
from models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.name == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('profile'))
        flash('Неверное имя пользователя или пароль. Попробуйте ещё раз')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.name == form.username.data).first()
        if user:
            flash("Это имя пользователя уже занято")
            return redirect(url_for('register'))
        user = User()
        user.name = form.username.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)

@app.route('/profile/')
def profile():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    return render_template('profile.html')

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/edit/competition/') #<int:competition_id>
def edit_competition(): #competition_id: int
    return render_template('edit_competition.html')
    

@app.route('/remove/task/') #<int:task_id>
def remove_task(): #task_id: int
    return

@app.route('/remove/competition/') #<int:competition_id>
def remove_competition(): #competition_id: int
    return