from flask import Flask
from models import db
from routes.main import main_bp
import os
from dotenv import load_dotenv
from flask_login import LoginManager
from models.todo import User

app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_URI", "sqlite:///todo.db")

db.init_app(app)

with app.app_context():
    db.create_all()
     
app.register_blueprint(main_bp)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main_bp.login'  # Redirect unauthorized users here

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

if __name__ == "__main__":
    app.run(debug=True)