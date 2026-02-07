import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='Admin!00', database='secure_web_app')
cur = conn.cursor()

print('COLUMNS:')
cur.execute('SHOW COLUMNS FROM users')
for row in cur.fetchall():
    print(row)

print('\nLATEST USERS:')
cur.execute('SELECT id, email, reset_token IS NOT NULL AS has_token, reset_token, reset_token_expiry FROM users ORDER BY id DESC LIMIT 10')
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()
