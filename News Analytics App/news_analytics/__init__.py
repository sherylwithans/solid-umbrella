from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY']='6d1e8594479d1c05c45289637b64f58f'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from news_analytics import routes



