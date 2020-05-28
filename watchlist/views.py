
from flask import render_template
from flask import request, redirect, flash
from flask import url_for
from flask_login import login_user, login_required, logout_user, current_user
from watchlist import app, db
from watchlist.models import User, Movie, File


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash("Invalid Input.")
            return redirect(url_for('login'))
        else:
            user = User.query.first()
            if username == user.username and user.validate_password(password):
                login_user(user)
                flash('Login Success.')
                return redirect(url_for('index'))
            else:
                flash('Invalid username or password.')
                return redirect(url_for('login'))
    else:
        return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    #logout
    logout_user()
    flash("Goodbye.")
    return redirect(url_for('index'))




@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        user = User.query.first()
        movies = Movie.query.all()
        return render_template('index.html', movies=movies)
    elif request.method == 'POST':
        #require login to operate
        if not current_user.is_authenticated:
            flash("please login...")
            return redirect(url_for('index'))

        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid Input.')
            return redirect(url_for('index'))
        else:
            movie = Movie(title=title, year=year)
            db.session.add(movie)
            db.session.commit()
            flash('Item Created.')
            return redirect(url_for('index'))


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash("Invalid Input.")
            return redirect(url_for('edit', movie_id=movie_id))
        else:
            movie.title = title
            movie.year = year
            db.session.commit()
            flash("Item Updated.")
            return redirect(url_for('index'))

    return render_template('edit.html', movie=movie)


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash("Item deleted.")
    return redirect(url_for('index'))


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash("Invalid Input.")
            return redirect(url_for('settings'))
        else:
            current_user.name = name
            #user = User.query.first()
            #user.name = name
            db.session.commit()
            flash('Settings Updated.')
            return redirect(url_for('index'))
    else:
        return render_template('settings.html')

@app.route('/Storage', methods=['GET', 'POST'])
@login_required
def storage():
    if request.method == 'POST':
        print('hi')
    else:
        files = File.query.all()
        return render_template('storage.html', files=files)
