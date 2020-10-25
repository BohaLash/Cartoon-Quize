from flask import Flask, render_template, redirect, url_for, request, redirect
import sqlite3
import random

app = Flask(__name__)

conn = sqlite3.connect('quize.db')
c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS questions(
        q TEXT,
        a1 TEXT,
        a2 TEXT,
        a3 TEXT
    )
""")
conn.commit()

c.execute("""
    CREATE TABLE IF NOT EXISTS answ(
        a INTENGER
    )
""")
conn.commit()


global a, q
a = {0: 1}
q = {0: 1}


@app.route('/', methods=['GET', 'POST'])
def main():
    global a, q
    if request.method == "POST":
        key = random.randrange(99999)
        while key in a.keys() or key in q.keys():
            key = random.randrange(99999)
        a[key] = 0
        q[key] = 0
        return redirect('/q/' + str(key))
    return render_template("index.html")


@app.route('/q/<n>', methods=["GET", "POST"])
def question(n):
    global a, q
    if request.method == "POST":
        answ = request.form['answ']
        a[n] += answ
        q[n] += 1
        return redirect('/q/' + str(n))
    with sqlite3.connect("quize.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM questions WHERE rowid = ?", (q[int(n)], ))  #
        row = data.fetchone()
        question = str(row[0])
        answs = [str(row[1]), str(row[2]), str(row[3])]
    return render_template("question.html", question=question, answ=answs)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
