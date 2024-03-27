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
@login_required
def profile():
    # user_zelenchuk = User()
    # user_zelenchuk.name = 'Зеленчук Илья Валерьевич МММММ'
    # user_zelenchuk.set_password('zelenchuk')
    # competition_by_zelenchuk = Competition()
    # competition_by_zelenchuk.author = user_zelenchuk
    # competition_by_zelenchuk.title = 'Соревнование Зеленчука И.В. МММММ'
    # competition_by_zelenchuk.tasks_count = 10
    # competition_by_zelenchuk.points_count = 1000
    # db.session.add_all([user_zelenchuk, competition_by_zelenchuk])
    # db.session.commit()
    # participant_admin = Participant()
    # participant_admin.competition_id = competition_by_zelenchuk.id
    # participant_admin.user_id = current_user.id
    # participant_admin.tasks_done = 5
    # participant_admin.points_collected = 500
    # db.session.add(participant_admin)
    # db.session.commit()
    # my_competition = Competition()
    # my_competition.author = current_user
    # my_competition.title = 'Моё соревнование'
    # my_competition.participants_count = 15
    # db.session.add(my_competition)
    # db.session.commit()
    user_competitions_info = [dict(zip(['tasks_done', 'competition_tasks_count', 'points_collected', 'competition_points_count', 'competition_id', 'competition_title', 'competition_organizer_name'], usr_comp_info)) for usr_comp_info in db.session.query(Participant.tasks_done, Competition.tasks_count, Participant.points_collected, Competition.points_count, Competition.id, Competition.title, Competition.organizer_name).join(Competition).filter(Participant.user_id == current_user.id and Competition.id == Participant.competition_id).all()]
    user_organized_competitions_info = [dict(zip(['competition_id', 'competition_title', 'participants_count', 'invite_ref'], usr_comp_info)) for usr_comp_info in db.session.query( Competition.id, Competition.title, Competition.participants_count, Competition.invite_ref).filter(Competition.organizer_name == current_user.name)]
    # db.session.delete(participant_admin)
    # db.session.delete(competition_by_zelenchuk)
    # db.session.delete(user_zelenchuk)
    # db.session.delete(my_competition)
    # db.session.commit()
    print(user_competitions_info)
    # user_competitions_info = current_user.competitions_info()
    # organizators_and_competition_references = [db.session.query(Competition.organizer_name, Competition.invite_ref).filter(Competition.id == participant_info.competition_id).first()
    #                                            for participant_info in user_competitions_info]
    return render_template('profile.html',
                           username = current_user.name,
                           user_competitions_info = user_competitions_info,
                           user_organized_competitions_info = user_organized_competitions_info,
                           )

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/competition/<int:id>')
@login_required
def competition(id: int):
    if db.session.query(Participant).filter(Participant.competition_id == id and Participant.user_id == current_user.id).first():
        return render_template('competition.html')
    return redirect(url_for('profile'))

@app.route('/edit/competition/') #<int:competition_id>
def edit_competition(): #competition_id: int
    return render_template('edit_competition.html')

@app.route('/remove/task/') #<int:task_id>
def remove_task(): #task_id: int
    return

@app.route('/remove/competition/') #<int:competition_id>
def remove_competition(): #competition_id: int
    return