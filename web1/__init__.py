from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

app.config['SECRET_KEY'] = "secretkey1"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
Bootstrap(app)
app.app_context().push()

from web1.routes import *
