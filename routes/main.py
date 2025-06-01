from flask import Blueprint, render_template, request, redirect, url_for, flash , current_app
from models import db
from models.todo import Todo , User
from flask_login import current_user, login_required , login_user , logout_user
from werkzeug.security import generate_password_hash, check_password_hash


main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/" , methods = ["GET" , "POST"])
@login_required
def home():
    try:
        if request.method == "POST":
            title = request.form.get('title')
            desc = request.form.get('desc')
            todo = Todo(title=title, desc=desc, user_id=current_user.id)
            db.session.add(todo)
            db.session.commit()
            flash("Todo Added Succesfully")
            return redirect(url_for('main_bp.home'))
        allTodos = Todo.query.filter_by(user_id=current_user.id).all()
        return render_template("index.html", allTodos = allTodos , username=current_user.username)
    except Exception as e:
        current_app.logger.error(f"error in home(): {e}")
        flash("Something went wrong. Please try again later.", "danger")
        return redirect(url_for('main_bp.home'))



@main_bp.route('/update/<int:sno>' , methods = ["GET" , "POST"])
@login_required
def update(sno):
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            desc = request.form.get('desc')
            todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            flash("Todo updated Succesfully")
            return redirect(url_for('main_bp.home'))
        todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
        return render_template("update.html" , todo=todo)
    except Exception as e:
        current_app.logger.error(f"error in update():{e}")
        flash("Something went wrong. Please try again later.", "danger")
        return redirect(url_for('main_bp.home'))
        

@main_bp.route('/delete/<int:sno>')
@login_required
def delete(sno):
    try:
        todo = Todo.query.filter_by(sno=sno, user_id=current_user.id).first_or_404()
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted Succesfully")
        return redirect("/")
    except Exception as e:
        current_app.logger.error(f"error in delete():{e}")
        flash("Something went wrong. Please try again later", "danger")
        return redirect(url_for('main_bp.home'))
        
@main_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if User.query.filter_by(username=username).first():
            return render_template("sign_up.html", error="Username already taken!")

        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("main_bp.login"))
    
    return render_template("sign_up.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("main_bp.home"))
        else:
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main_bp.home"))
