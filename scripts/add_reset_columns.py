import mysql.connector

conn = mysql.connector.connect(host='localhost', user='root', password='Admin!00', database='secure_web_app')
cur = conn.cursor()

# Check and add reset_token
cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s", ('secure_web_app','users','reset_token'))
if cur.fetchone()[0] == 0:
	cur.execute("ALTER TABLE users ADD COLUMN reset_token VARCHAR(255)")
	print('Added reset_token')
else:
	print('reset_token already exists')

# Check and add reset_token_expiry
cur.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=%s AND table_name=%s AND column_name=%s", ('secure_web_app','users','reset_token_expiry'))
if cur.fetchone()[0] == 0:
	cur.execute("ALTER TABLE users ADD COLUMN reset_token_expiry DATETIME")
	print('Added reset_token_expiry')
else:
	print('reset_token_expiry already exists')

conn.commit()
cur.close()
conn.close()
