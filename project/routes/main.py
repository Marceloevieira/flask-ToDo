from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .. import db
from ..models import Task, User, Category

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def home_index():
    return render_template('home/index.html')


# Routes Task

@main.route('/tasks', methods=['GET', 'POST'])
@login_required
def task_index():
    """root route"""
    if request.method == 'POST':
        task = Task(
            description=request.form['description'], category_id=request.form['category_id'], status=request.form[
                'status'], expect_hours=request.form['expect_hours'], expect_performed=request.form['expect_performed'],
            user_id=current_user.id)
        try:
            db.session.add(task)
            db.session.commit()
            return redirect('/tasks')
        except:
            return "Houve um erro, ao inserir a tarefa"
    else:
        tasks = Task.query.filter_by(
            user_id=current_user.id).order_by(Task.date_created).all()
        categories = Category.query.order_by(Category.date_created).all()
        return render_template('task/index.html', tasks=tasks, categories=categories)


@main.route('/tasks/delete/<int:id>')
def task_delete(id):
    """delete a task"""
    task = Task.query.get_or_404(id)
    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/tasks')
    except:
        return "Houve um erro, ao inserir a tarefa"


@main.route('/tasks/update/<int:id>', methods=['GET', 'POST'])
def task_update(id):
    """update route"""
    task = Task.query.get_or_404(id)
    categories = Category.query.order_by(Category.date_created).all()
    if request.method == 'POST':
        task.description = request.form['description']
        task.category_id = request.form['category_id']
        task.status = request.form['status']
        task.expect_hours = request.form['expect_hours']
        task.expect_performed = request.form['expect_performed']
        try:
            db.session.commit()
            return redirect('/tasks')
        except:
            return "Houve um erro, ao atualizar a tarefa"
    else:
        return render_template('task/update.html', task=task, categories=categories)


# Routes Category


@main.route('/categories', methods=['GET', 'POST'])
# @login_required
def category_index():
    """root route"""
    if request.method == 'POST':
        category = Category(
            description=request.form['description'])
        try:
            db.session.add(category)
            db.session.commit()
            return redirect('categories')
        except:
            return "Houve um erro, ao inserir a tarefa"
    else:
        categories = Category.query.order_by(Category.date_created).all()
        return render_template('category/index.html', categories=categories)


@main.route('/categories/delete/<int:id>')
def category_delete(id):
    """delete a categories"""
    category = Category.query.get_or_404(id)
    try:
        db.session.delete(category)
        db.session.commit()
        return redirect('/categories')
    except:
        return "Houve um erro, ao inserir a tarefa"


@main.route('/categories/update/<int:id>', methods=['GET', 'POST'])
def category_update(id):
    """update route"""
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.description = request.form['description']

        try:
            db.session.commit()
            return redirect('/categories')
        except:
            return "Houve um erro, ao atualizar a tarefa"
    else:
        return render_template('category/update.html', category=category)
