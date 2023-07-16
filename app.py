import os

from flask import Flask, render_template
# from flask_session import Session
# from tempfile import mkdtemp
# from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')






if __name__ == "__main__":
    app.run(debug=True)