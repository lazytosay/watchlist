from flask import Flask, render_template
from flask import request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
import os
import sys
import click

app = Flask(__name__)
app.secret_key = "dev"

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


#register as command in the cmd
@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    #init the database
    if drop:
        click.echo("dropping..")
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')

@app.cli.command()
def forge():
    #generate fake data
    db.create_all()

    name = 'bill'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo("Done..generated fake data")


@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user = User.query.first()
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)
    elif request.method == 'POST':
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid Input...')
            return redirect(url_for('index'))
        else:
            movie = Movie(title=title, year=year)
            db.session.add(movie)
            db.session.commit()
            flash('Item Created.')
            return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    user = User.query.first()
    return render_template('404.html'), 404

@app.route('/usr/<name>')
def user_page(name):
    return 'User: %s' % name













if __name__ == "__main__":
    #app.run(debug=True, host='192.168.1.103')
    app.run(debug=True)

