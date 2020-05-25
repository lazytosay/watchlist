from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'welcome to my watchlist'


if __name__ == "__main__":
    #app.run(debug=True, host='192.168.1.103')
    app.run(debug=True)
