import mysql.connector
import secrets
from datetime import datetime, timedelta

EMAIL = 'abcd@gmail.com'

conn = mysql.connector.connect(host='localhost', user='root', password='Admin!00', database='secure_web_app')
cur = conn.cursor(dictionary=True)

cur.execute('SELECT * FROM users WHERE email=%s', (EMAIL,))
user = cur.fetchone()
if not user:
    print('User not found')
else:
    reset_token = secrets.token_urlsafe(32)
    expiry = datetime.now() + timedelta(hours=1)
    cur.execute('UPDATE users SET reset_token=%s, reset_token_expiry=%s WHERE email=%s', (reset_token, expiry, EMAIL))
    conn.commit()
    print('Set token for', EMAIL)
    print('Token:', reset_token)
    cur.execute('SELECT id, email, reset_token, reset_token_expiry FROM users WHERE email=%s', (EMAIL,))
    print(cur.fetchone())

cur.close()
conn.close()
