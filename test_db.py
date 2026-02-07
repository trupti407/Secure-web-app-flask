import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Admin!00",
    database="secure_web_app"
)

print("Database connected successfully!")
conn.close()
