from flask import Flask
from flask import url_for
app = Flask(__name__)

@app.route('/')
@app.route('/about')
def hello():
    return u'你好welcome to my watchlist'

@app.route('/usr/<name>')
def user_page(name):
    return 'User: %s' % name













if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.103')
    #app.run(debug=True)

