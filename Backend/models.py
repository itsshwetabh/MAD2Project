from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from sqlalchemy.sql import func
import pytz
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    fs_uniquifier = db.Column(db.String, unique = True, nullable = False)
    active = db.Column(db.Boolean, default = True)
    roles = db.Relationship('Role', backref = 'bearers', secondary='user_roles')

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, unique = True, nullable  = False)
    description = db.Column(db.String, nullable = False)

class UserRoles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    subject = db.relationship('Subject', backref=db.backref('chapters', lazy=True))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False, default=func.current_date()) 
    time_duration = db.Column(db.Time, nullable=False)  
    chapter = db.relationship('Chapter', backref=db.backref('quizzes', lazy=True))
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_title = db.Column(db.String(255), nullable=False) 
    question_statement = db.Column(db.Text, nullable=False)  
    option_1 = db.Column(db.String, nullable=False)
    option_2 = db.Column(db.String, nullable=False)
    option_3 = db.Column(db.String, nullable=False)
    option_4 = db.Column(db.String, nullable=False)
    correct_option = db.Column(db.String, nullable=False)  
    marks = db.Column(db.Integer, nullable=False)  
    created_at = db.Column(db.DateTime, default=func.now())  

    quiz = db.relationship('Quiz', backref=db.backref('questions', lazy=True))




class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    score = db.Column(db.Integer, nullable=True)  # Null means attempt in progress
    max_score = db.Column(db.Integer, nullable=True)
    started_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(pytz.timezone("Asia/Kolkata")))  
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)  # Set when user finishes the quiz
    total_time_taken = db.Column(db.Integer, nullable=True)  # Time in seconds
    user = db.relationship('User', backref=db.backref('attempts', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('attempts', lazy=True))
    responses = db.Column(db.JSON, nullable=True)


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('quiz_attempt.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    selected_option = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    attempt = db.relationship('QuizAttempt', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('user_answers', lazy=True))

