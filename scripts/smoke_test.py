import os
import sys
import time
import uuid
import mysql.connector
from pathlib import Path
# Ensure project root is on sys.path so local modules import correctly
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))
from config import db_config

# Ensure schema and reset columns
print('Running DB migration (schema.sql) ...')
conn = mysql.connector.connect(**db_config)
cur = conn.cursor()
with open(os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql'), 'r') as f:
    sql = f.read()
for stmt in sql.split(';'):
    if stmt.strip():
        try:
            cur.execute(stmt)
        except Exception:
            pass
conn.commit()

# ensure reset columns exist
cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s", (db_config.get('database'), 'users', 'reset_token'))
if cur.fetchone()[0] == 0:
    cur.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)")
    print('Added reset_token')
cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s", (db_config.get('database'), 'users', 'reset_token_expiry'))
if cur.fetchone()[0] == 0:
    cur.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME")
    print('Added reset_token_expiry')
conn.commit()
cur.close()
conn.close()

print('Starting Flask test client smoke tests...')
from app import app

# Disable CSRF for test client
app.config['WTF_CSRF_ENABLED'] = False

client = app.test_client()

username = f'smoke_{uuid.uuid4().hex[:8]}'
email = f'{username}@example.test'
password = 'Password123!'

print('Registering user:', username, email)
resp = client.post('/register', data={'username': username, 'email': email, 'password': password}, follow_redirects=True)
print('Register status code:', resp.status_code)

print('Logging in...')
resp = client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)
print('Login status code:', resp.status_code)

print('Requesting password reset...')
resp = client.post('/forgot', data={'email': email}, follow_redirects=True)
print('Forgot response status:', resp.status_code)

# Check DB for token
conn = mysql.connector.connect(**db_config)
cur = conn.cursor(dictionary=True)
cur.execute('SELECT id, reset_token FROM users WHERE email=%s', (email,))
row = cur.fetchone()
if not row or not row.get('reset_token'):
    print('ERROR: reset_token was not set in DB for', email)
else:
    token = row['reset_token']
    print('Found token:', token[:8] + '...')
    # Reset the password using token
    new_pw = 'NewPass456!'
    resp = client.post(f'/reset/{token}', data={'password': new_pw, 'confirm_password': new_pw}, follow_redirects=True)
    print('/reset response status:', resp.status_code)

    # Try login with new password
    resp = client.post('/login', data={'username': username, 'password': new_pw}, follow_redirects=True)
    print('Login with new password status:', resp.status_code)

    # Cleanup: delete user
    cur.execute('DELETE FROM users WHERE id=%s', (row['id'],))
    conn.commit()
    print('Cleaned up test user')

cur.close()
conn.close()

print('Smoke tests completed')
