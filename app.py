from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
import sys

app = Flask(__name__)

#dealing with the database part
WIN = sys.platform.startswith("win")
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#table name will be user (lower case)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))





#FIXME: temp data to make sure template works
name = "Bill"
movies = [
    {'title': 'My Neighbor Totoro', 'year':'1988'},
    {'title': 'Dead Poets Society', 'year':'1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'}
]

@app.route('/')
@app.route('/about')
def index():
    return render_template('index.html', name=name, movies=movies)

@app.route('/usr/<name>')
def user_page(name):
    return 'User: %s' % name













if __name__ == "__main__":
    #app.run(debug=True, host='192.168.1.103')
    app.run(debug=True)

