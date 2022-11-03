from flask import Flask, redirect

def init():
    app = Flask(__name__)
    return app

@app.route("/")
def index():
    return redirect('https://fest.stepiveter.ru')



if __name__ == '__main__':
    init().run()