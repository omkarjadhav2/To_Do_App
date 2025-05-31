from flask import Blueprint, render_template, request, redirect, url_for, flash , current_app
from models import db
from models.todo import Todo

main_bp = Blueprint('main_bp', __name__)

@main_bp.route("/" , methods = ["GET" , "POST"])
def home():
    try:
        if request.method == "POST":
            title = request.form.get('title')
            desc = request.form.get('desc')
            todo = Todo(title = title , desc = desc)
            db.session.add(todo)
            db.session.commit()
            flash("Todo Added Succesfully")
            return redirect(url_for('main_bp.home'))
        allTodos = Todo.query.all()
        return render_template("index.html", allTodos = allTodos)
    except Exception as e:
        current_app.logger.error(f"error in home(): {e}")
        flash("Something went wrong. Please try again later.", "danger")
        return redirect(url_for('main_bp.home'))



@main_bp.route('/update/<int:sno>' , methods = ["GET" , "POST"])
def update(sno):
    try:
        if request.method == 'POST':
            title = request.form.get('title')
            desc = request.form.get('desc')
            todo = Todo.query.filter_by(sno=sno).first_or_404()
            todo.title = title
            todo.desc = desc
            db.session.add(todo)
            db.session.commit()
            flash("Todo updated Succesfully")
            return redirect(url_for('main_bp.home'))
        todo = Todo.query.filter_by(sno=sno).first_or_404()
        return render_template("update.html" , todo=todo)
    except Exception as e:
        current_app.logger.error(f"error in update():{e}")
        flash("Something went wrong. Please try again later.", "danger")
        return redirect(url_for('main_bp.home'))
        

@main_bp.route('/delete/<int:sno>')
def delete(sno):
    try:
        todo = Todo.query.filter_by(sno=sno).first_or_404()
        db.session.delete(todo)
        db.session.commit()
        flash("Todo deleted Succesfully")
        return redirect("/")
    except Exception as e:
        current_app.logger.error(f"error in delete():{e}")
        flash("Something went wrong. Please try again later", "danger")
        return redirect(url_for('main_bp.home'))
        
