from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def setup():
    token = request.form['x-gcp-marketplace-token']
    print("token is:")
    print(token)
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
