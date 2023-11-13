from flask import Flask, redirect, jsonify
from datetime import date

app = Flask(__name__)
port = 500

@app.route("/")
def index():
    return redirect("http://127.0.0.1:5000/info/", code=302)

@app.route('/info/')
def info():
    return '''send request to <a href=http://127.0.0.1:5000/info/{username}> </a>'''

@app.route('/info/<username>')
def infoByUserName(username):
    return jsonify(
        greeting=["hello", "world"],
        date=date.today(),
    )

if __name__ == '__main__':
    app.run(debug=True, port=port)
