from enum import unique
from operator import truediv

from sqlalchemy.orm import backref
from . import db
from flask_login import UserMixin
import sqlalchemy as sa
from alembic import op

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))


#Use classes to create the database from our ER Diagram

class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    instructors_id = db.Column(db.Integer) 
    dept_hed = db.relationship('Instructors', backref='instructor', uselist=False)


    def __repr__(self):
        return '<department %r>' % self.id


class Instructors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    dept_id = db.Column(db.Integer, db.ForeignKey('departments.id'))


    def __repr__(self):
        return '<instructor %r>' % self.id



class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    instructors_id = db.Column(db.Integer, db.ForeignKey('instructors.id')) 
    departments_id = db.Column(db.Integer, db.ForeignKey('departments.id')) 

    def __repr__(self):
        return '<courses %r>' % self.id



class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return '<students %r>' % self.id



class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    students_id = db.Column(db.Integer, db.ForeignKey('students.id')) 
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id')) 

    def __repr__(self):
        return '<student_courses %r>' % self.id

