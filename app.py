from flask import Flask, render_template
from flask import url_for
app = Flask(__name__)

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

