
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exist', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters', category='error')
        elif len(fullname) < 2:
            flash('Fullname must be greater than 1 character', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            new_user = User(email=email, full_name=fullname, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/instructors', methods=['GET', 'POST'])
def instructor():
    if request.method == 'POST':
        instructor_name = request.form['fullname']
        instructor_email = request.form['email']
        instructor_deptid = request.form['dept_id']
        new_instructor = Instructors(fullname=instructor_name, email=instructor_email, dept_id=instructor_deptid)

        try:
            db.session.add(new_instructor)
            db.session.commit()
            flash("New instructor added successfully", category='success')
            return redirect('/instructors')
        except:
            flash("Failed to add new instructor", category='error')

    else:
        instructor = Instructors.query.all()
        department = Departments.query.all()
        return render_template("instructors.html", user=current_user, instructor=instructor, department=department)

@auth.route('/instructors/delete/<int:id>')
def delete(id):
    int_to_delete = Instructors.query.get_or_404(id)

    try:
        db.session.delete(int_to_delete)
        db.session.commit()
        flash("Instructor deleted successfully", category='success')
        return redirect('/instructors')
    except:
        flash("Failed to delete instructor", category='error')

@auth.route('/instructors/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    instructor = Instructors.query.get_or_404(id)

    if request.method == 'POST':
        instructor.fullname = request.form['fullname']
        instructor.email = request.form['email']
        instructor.dept_id = request.form['dept_id']

        try:
            db.session.commit()
            flash("Instructor updated successfully", category='success')
            return redirect('/instructors')
        except:
            flash("There was an issue updating instructor", category='error')
    else:
        return render_template('updateInstructor.html', instructor=instructor, user=current_user)
    return redirect('/instructors')
    



@auth.route('/courses', methods=['GET', 'POST'])
def course():
    if request.method == 'POST':
        course_name = request.form['name']
        course_instructor = request.form['instructors_id']
        course_dept = request.form['departments_id']
        new_course = Courses(name=course_name, instructors_id=course_instructor, departments_id=course_dept)

        try:
            db.session.add(new_course)
            db.session.commit()
            flash("New course added successfully", category='success')
            return redirect('/courses')
        except:
            flash("Failed to add new course", category='error')

    else:
        courses = Courses.query.all()
        instructor = Instructors.query.all()
        department = Departments.query.all()
        return render_template("courses.html", user=current_user, courses=courses, instructor=instructor, department=department)

@auth.route('/courses/delete/<int:id>')
def delete2(id):
    course_to_delete = Courses.query.get_or_404(id)

    try:
        db.session.delete(course_to_delete)
        db.session.commit()
        flash("Course deleted successfully", category='success')
        return redirect('/courses')
    except:
        flash("Failed to delete course", category='error')

@auth.route('/courses/update/<int:id>', methods=['GET', 'POST'])
def update2(id):
    course = Courses.query.get_or_404(id)

    if request.method == 'POST':
        course.name = request.form['name']
        course.instructors_id = request.form['instructors_id']
        course.departments_id = request.form['departments_id']

        try:
            db.session.commit()
            flash("Course updated successfully", category='success')
            return redirect('/courses')
        except:
            flash("There was an issue updating course", category='error')
    else:
        return render_template('updateCourses.html', course=course, user=current_user)


@auth.route('/students', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        student_name = request.form['fullname']
        student_email = request.form['email']
        new_student = Students(fullname=student_name, email=student_email)

        try:
            db.session.add(new_student)
            db.session.commit()
            flash("New student added successfully", category='success')
            return redirect('/students')
        except:
            flash("Failed to add new student", category='error')

    else:
        students = Students.query.all()
        return render_template("students.html", user=current_user, students=students)


@auth.route('/students/delete/<int:id>')
def delete3(id):
    std_to_delete = Students.query.get_or_404(id)

    try:
        db.session.delete(std_to_delete)
        db.session.commit()
        flash("Student deleted successfully", category='success')
        return redirect('/students')
    except:
        flash("Failed to delete student", category='error')

@auth.route('/students/update/<int:id>', methods=['GET', 'POST'])
def update3(id):
    student = Students.query.get_or_404(id)

    if request.method == 'POST':
        student.fullname = request.form['name']
        student.email = request.form['email']

        try:
            db.session.commit()
            flash("Student updated successfully", category='success')
            return redirect('/students')
        except:
            flash("There was an issue updating course", category='error')
    else:
        return render_template('updateStudents.html', student=student, user=current_user)
