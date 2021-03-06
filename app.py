from flask import Flask, render_template, redirect, request
import sqlite3
import random

app = Flask(__name__)

# db initialization
conn = sqlite3.connect('quiz.db')
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


global a, q, m
a = {}
q = {}
m = {}


@app.route('/', methods=['GET', 'POST'])
def main():
    global a, q, m
    # starting quize
    if request.method == "POST":
        # generate user hash
        key = random.randrange(99999)
        while key in a.keys() or key in q.keys():
            key = random.randrange(99999)
        a[key] = 0
        q[key] = 1
        m[key] = 'Good Luck!'
        return redirect('/q/' + str(key))
    return render_template("index.html")


@app.route('/q/<n>', methods=["GET", "POST"])
def question(n):
    global a, q, m
    # on invalid user hesh
    if not (int(n) in a.keys() or int(n) in q.keys() or int(n) in m.keys()):
        return redirect('/')
    # on resiving answer
    if request.method == "POST":
        answ = int(request.form['a'])
        # get true answer
        with sqlite3.connect("quiz.db") as con:
            cur = con.cursor()
            data = cur.execute(
                "SELECT * FROM answ WHERE rowid = ?", (q[int(n)], ))
            t = int(data.fetchone()[0])
        # if answ is true
        if answ == t:
            a[int(n)] += 1
            m[int(n)] = 'Good job!'
        else:
            # get right answ from db
            with sqlite3.connect("quiz.db") as con:
                cur = con.cursor()
                data = cur.execute(
                    "SELECT * FROM questions WHERE rowid = ?", (q[int(n)], ))
                row = data.fetchone()
                # put it in messaage
                m[int(n)] = 'Your made a mistake! The correct answer was: ' + \
                    str(row[t + 1])
        q[int(n)] += 1
        return redirect(f'/q/{str(n)}' if q[int(n)] <= 48 else f'/res/{str(n)}')
    # get question and answers
    with sqlite3.connect("quiz.db") as con:
        cur = con.cursor()
        data = cur.execute(
            "SELECT * FROM questions WHERE rowid = ?", (q[int(n)], ))
        row = data.fetchone()
        question = str(row[0])
        answs = [str(row[1]), str(row[2]), str(row[3]), str(row[4])]
    return render_template("question.html", question=question, answ=answs, res=a[int(n)], message=m[int(n)])


@app.route('/res/<n>', methods=["GET", "POST"])
def result(n):
    global a, q, m
    # on invalid user hesh or button click
    if not (int(n) in a.keys() or int(n) in q.keys() or int(n) in m.keys()) or request.method == "POST":
        return redirect('/')
    q.pop(int(n))
    m.pop(int(n))
    return render_template("result.html", res=a.pop(int(n)))


if __name__ == "__main__":
    app.run(debug=True)
