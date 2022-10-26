from flask import Flask
from flask import render_template
from flask import url_for
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    print(url_for('static', filename='templates/assets/css/style.css'))
    return render_template('/index.html')

@app.route("/order", methods=["POST"])
def order():
    pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    