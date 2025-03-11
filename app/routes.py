from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Task
from app import db
from app.forms import RegistrationForm, LoginForm, TaskForm


main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


auth_routes = Blueprint('auth', __name__)

@auth_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        role = form.role.data


        user = User.query.filter_by(email=email).first()
        if user:
            flash('Пользователь с таким email уже зарегистрирован.', 'error')
            return redirect(url_for('auth.register'))


        new_user = User(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно! Пожалуйста, войдите.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data


        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Неверный email или пароль.', 'error')
    return render_template('login.html', form=form)

@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'success')
    return redirect(url_for('main.index'))


task_routes = Blueprint('task', __name__)

@task_routes.route('/add_task', methods=['GET', 'POST'])
@login_required
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        category = form.category.data
        due_date = form.due_date.data


        new_task = Task(
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            is_completed=False,
            user_id=current_user.id
        )


        db.session.add(new_task)
        db.session.commit()

        flash('Задача успешно добавлена!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_task.html', form=form)

@task_routes.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)


    if task.user_id != current_user.id:
        flash('У вас нет прав на удаление этой задачи.', 'error')
        return redirect(url_for('main.index'))


    db.session.delete(task)
    db.session.commit()

    flash('Задача успешно удалена!', 'success')
    return redirect(url_for('main.index'))

@task_routes.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)

    if task.user_id != current_user.id:
        flash('У вас нет прав на изменение этой задачи.', 'error')
        return redirect(url_for('main.index'))


    task.is_completed = True
    db.session.commit()

    flash('Задача отмечена как выполненная!', 'success')
    return redirect(url_for('main.index'))