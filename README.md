# 🔐 Secure Web Application – Flask

A secure, modern Flask authentication application developed as part of the  
**Cryptonic Area’s Cyber Security Virtual Internship Program**.

The objective of this project is to practically implement **secure coding practices** and **web application security concepts** used in real-world systems.  
This project focuses on building a secure authentication system while protecting against common web vulnerabilities such as **SQL Injection, Cross-Site Scripting (XSS), password-based attacks, CSRF, and session hijacking**.

---

# 🎯 Project Objectives

- Build a secure web application using Flask
- Implement authentication and session management securely
- Apply password hashing and strong password policies
- Protect the application against common web attacks
- Follow industry-level security best practices

---

# ✨ Features

# 👤 Authentication & Authorization
- Secure user registration
- Duplicate username/email prevention
- Login & logout with session protection
- Dashboard access restricted to authenticated users only

# 🔑 Password Security
- Password hashing using **PBKDF2 + SHA256 (Werkzeug)**
- Minimum password length validation
- Confirm-password validation

# 📧 Secure Password Reset
- Token-based forgot-password flow
- Token expiry set to **1 hour**
- Email delivery via SMTP
- Development fallback link when SMTP is not configured

# 🛡️ Web Security Controls
- CSRF protection using **Flask-WTF**
- SQL Injection prevention via **parameterized queries**
- XSS mitigation via input validation & Jinja2 auto-escaping
- Secure session cookies:
  - `HttpOnly`
  - `Secure`
  - `SameSite=Lax`
- Session cleared properly on logout

# 🎨 User Interface
- Bootstrap 5 responsive UI
- Centered authentication cards
- Flash messages for user-friendly feedback
- Clean and modern design

---

# 🧠 Threat Model & Protection Mapping

| Threat | Protection Implemented |
|------|------------------------|
| SQL Injection | Parameterized MySQL queries |
| Cross-Site Scripting (XSS) | Input validation & Jinja2 auto-escaping |
| Password Attacks | PBKDF2 hashing with salting |
| Session Hijacking | Secure cookies & session clearing |
| CSRF Attacks | Flask-WTF CSRF tokens |
| Account Enumeration | Generic forgot-password messages |

---

# 🛠️ Tech Stack

- **Backend:** Flask (Python)
- **Database:** MySQL
- **Frontend:** HTML, Bootstrap 5, CSS
- **Security:** Flask-WTF, Werkzeug, dotenv
- **Email:** SMTP (TLS / STARTTLS)

---

# ⚙️ Setup & Installation (Windows)


#**1️⃣ Create Virtual Environment**

python -m venv .venv

.\.venv\Scripts\Activate.ps1


#**2️⃣ Install Dependencies**

python -m pip install -r requirements.txt


#**3️⃣ Environment Configuration**

Create a .env file in the root directory:

DB_HOST=localhost

DB_USER=root

DB_PASSWORD=your_password

DB_NAME=secure_web_app

SECRET_KEY=your_secure_random_key

SMTP_HOST=smtp.example.com

SMTP_PORT=587

SMTP_USER=your_email

SMTP_PASSWORD=your_password

SMTP_FROM=your_email

SMTP_USE_TLS=True

DEV_MODE=True


⚠️ Never commit .env to GitHub
(.gitignore already includes it)


#**4️⃣ Database Setup**

Run schema manually:

mysql -u root -p < database/schema.sql


OR use helper script:

python scripts/add_reset_columns.py


#**5️⃣ Run the Application**

python app.py


Open in browser:

👉 http://localhost:5000


**#🔁 Password Reset Flow**

User clicks Forgot Password

Enters registered email

Secure reset token generated

Reset link sent via email (or shown in dev mode)

Token expiry validated

Password updated securely

**#📁 Project Structure**

pgsql

Copy code

Secure-web-app-flask/

├── app.py

├── config.py

├── .env                 # Not committed

├── requirements.txt

├── README.md

├── SECURITY_DESIGN.md

├── database/

│   └── schema.sql

├── templates/

│   ├── login.html

│   ├── register.html

│   ├── forgot.html

│   ├── reset.html

│   ├── dashboard.html

│   └── email/

│       └── reset_password.html

└── static/

    └── style.css
    

**#📸 Application Screenshots**

🔐 Login Page

screenshots/login.png

📝 Register Page

screenshots/register.png

🔑 Forgot Password

screenshots/forgot.png

🔁 Password Reset

📊 User Dashboard


**#🧪 Troubleshooting**

reset_token column missing
→ Run scripts/add_reset_columns.py

CSRF error
→ Ensure {{ csrf_token() }} is present in all forms

SMTP not sending mail
→ Verify SMTP credentials & network access

Login loop after logout
→ Sessions are cleared using session.clear()

**#🚀 Future Enhancements**

Role-based access control (Admin / User)

Login rate limiting (Flask-Limiter)

Email verification on registration

Two-Factor Authentication (2FA)

Security audit logging


**#✅ Project Status**

✔ Secure authentication implemented

✔ Web security threats mitigated

✔ Internship requirements fulfilled

✔ Ready for GitHub, mentor review & resume


**#👩‍💻 Author**

Trupti Lavate

Cybersecurity & Python | Flask Developer


This project was developed as part of the Cryptonic Area’s Cyber Security Virtual Internship Program to gain hands-on experience in secure web application development.

