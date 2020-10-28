import sqlite3

# input()
q = str(input())
input()
a1 = str(input())
a2 = str(input())
a3 = str(input())
a4 = str(input())
# input()
input()

print('Question: ' + q)
print('A: ' + a1[4:])
print('B: ' + a2[4:])
print('C: ' + a3[4:])
print('D: ' + a4[4:])

conn = sqlite3.connect('quize.db')
c = conn.cursor()

c.execute("INSERT INTO questions VALUES (?, ?, ?, ?, ?)", (q[1:], a1[4:], a2[4:], a3[4:], a4[4:]))
conn.commit()
