from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('social_network.db')
c = conn.cursor()


@app.route("/<n>", methods=['GET', 'POST'])
def main(n):
    q = 'hello'
    a = ['a', 'b', 'c']
    return render_template('index.html', question=q, answ = a)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
