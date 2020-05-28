import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'dev'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')

#for compatibility
WIN = sys.platform.startswith("win")
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

#app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#for upload files
UPLOAD_FOLDER = os.path.join(app.root_path, 'storage')
print(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user

login_manager.login_view='login'

@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


@app.context_processor
def inject_storage_info():
    from watchlist.models import Storage
    storage = Storage.query.first()
    if not storage:
        storage = Storage(total=300*1024*1024, available=300*1024*1024, taken=0)
        db.session.add(storage)
        db.session.commit()
    return dict(storage=storage)

from watchlist import views, errors, commands
