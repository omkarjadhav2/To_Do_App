from flask import Flask
from models import db
from routes.main import main_bp
import os
from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQL_URI", "sqlite:///todo.db")

db.init_app(app)

with app.app_context():
    db.create_all()
     
app.register_blueprint(main_bp)


if __name__ == "__main__":
    app.run(debug=False)