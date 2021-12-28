from flask import Blueprint, render_template, request,redirect, flash
from flask_login import login_required, current_user
from .models import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        department_name = request.form['name']
        dept_head = request.form['instructor']
        new_dept = Departments(name=department_name, instructors_id=dept_head)

        try:
            db.session.add(new_dept)
            db.session.commit()
            flash("New department added successfully", category='success')
            return redirect('/')
        except:
            flash("Failed to add new department", category='error')

    else:
        department = Departments.query.all()
        instruct = Instructors.query.all()
        return render_template("home.html", user=current_user, department=department, instruct=instruct)

@views.route('/delete/<int:id>')
def delete(id):
    dept_to_delete = Departments.query.get_or_404(id)

    try:
        db.session.delete(dept_to_delete)
        db.session.commit()
        flash("Department deleted successfully", category='success')
        return redirect('/')
    except:
        flash("Failed to delete department", category='error')

@views.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    department = Departments.query.get_or_404(id)

    if request.method == 'POST':
        department.name = request.form['name']
        department.instructors_id = request.form['instructor']

        try:
            db.session.commit()
            flash("Department updated successfully", category='success')
            return redirect('/')
        except:
            flash("There was an issue updating department", category='error')
    else:
        return render_template('updateDept.html', department=department, user=current_user)

