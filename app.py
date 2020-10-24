from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('social_network.db')
c = conn.cursor()


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/login", methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    print(login, password)

    if login and password:
        message = "Wrong username or password"
    else:
        message = "Enter login and password"

    return render_template('login.html', message=message)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
