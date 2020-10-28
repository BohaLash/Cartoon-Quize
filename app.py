from flask import Flask, render_template, redirect, url_for, request, redirect
import sqlite3
import random

app = Flask(__name__)

conn = sqlite3.connect('quize.db')
c = conn.cursor()

# c.execute("""
#     CREATE TABLE IF NOT EXISTS questions(
#         q TEXT,
#         a1 TEXT,
#         a2 TEXT,
#         a3 TEXT,
#         a4 TEXT
#     )
# """)
# conn.commit()

# c.execute("""
#     CREATE TABLE IF NOT EXISTS answ(
#         a INTENGER
#     )
# """)
# conn.commit()


global a, q
a = {}
q = {}


@app.route('/', methods=['GET', 'POST'])
def main():
    global a, q
    if request.method == "POST":
        key = random.randrange(99999)
        while key in a.keys() or key in q.keys():
            key = random.randrange(99999)
        a[key] = 0
        q[key] = 1
        return redirect('/q/' + str(key))
    return render_template("index.html")


@app.route('/q/<n>', methods=["GET", "POST"])
def question(n):
    global a, q
    if not (int(n) in a.keys() or int(n) in q.keys()):
        return redirect('/')
    if request.method == "POST":
        answ = int(request.form['a'])
        with sqlite3.connect("quize.db") as con:
            cur = con.cursor()
            data = cur.execute(
                "SELECT * FROM answ WHERE rowid = ?", (q[int(n)], ))
        t = int(data.fetchone()[0])
        if answ == t:
            a[int(n)] += 1
        q[int(n)] += 1
        return redirect(f'/q/{str(n)}' if q[int(n)] <= 48 else f'/res/{str(n)}')
    with sqlite3.connect("quize.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM questions WHERE rowid = ?", (q[int(n)], ))
        row = data.fetchone()
        question = str(row[0])
        answs = [str(row[1]), str(row[2]), str(row[3]), str(row[4])]
    return render_template("question.html", question=question, answ=answs)


@app.route('/res/<n>', methods=["GET", "POST"])
def result(n):
    global a, q
    if not (int(n) in a.keys() or int(n) in q.keys()) or request.method == "POST":
        return redirect('/')
    q.pop(int(n))
    return render_template("result.html", res=a.pop(int(n)))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
