from app import db,  login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))
    competitions_info = db.relationship('Participant', backref='user_info')
    tasks_info = db.relationship('TaskCompleteInfo', backref='user')
    organized_competitions = db.relationship('Competition', backref='author')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return db.session().query(User).get(user_id)

class Competition(db.Model):
    __tablename__ = 'competitions'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), unique=True)
    organizer_name = db.Column(db.String(255), db.ForeignKey('users.name'))
    tasks = db.relationship('Task', backref='competition')
    participants_info = db.relationship('Participant', backref='competition')
    participants_count = db.Column(db.Integer())
    tasks_count = db.Column(db.Integer())
    points_count = db.Column(db.Integer())
    invite_ref = db.Column(db.String(255))
    preparation = db.Column(db.Boolean())

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255))
    category = db.Column(db.String(255))
    points = db.Column(db.Integer())
    content = db.Column(db.Text())
    flag = db.Column(db.Text())
    tries = db.relationship('TaskCompleteInfo', backref='task')
    competition_id = db.Column(db.Integer(), db.ForeignKey('competitions.id'))

class Participant(db.Model):
    __tablename__ = 'participants'
    competition_id = db.Column(db.Integer(), db.ForeignKey('competitions.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    tasks_done = db.Column(db.Integer())
    points_collected = db.Column(db.Integer())

class TaskCompleteInfo(db.Model):
    __tablename__ = 'tasks_complete_info'
    task_id = db.Column(db.Integer(), db.ForeignKey('tasks.id'), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    result = db.Column(db.Boolean())