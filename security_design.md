# 🔐 Security Design Document
## Secure Web Application – Flask

This document explains the **security architecture, threat model, and protection mechanisms**
implemented in the Secure Web Application built using Flask and MySQL.

The goal of this project is to demonstrate **secure coding practices and threat hardening**
used in real-world production web applications.

---

## 🎯 Security Objectives

- Protect user credentials from theft and misuse
- Prevent common web attacks (SQL Injection, XSS, CSRF)
- Ensure secure session handling
- Implement safe authentication and password reset mechanisms
- Follow industry-standard security best practices

---

## 🧱 Authentication & Authorization Design

### User Authentication
- Users register using a **username, email, and password**
- Passwords are **never stored in plain text**
- Login is validated using securely hashed passwords

### Access Control
- Protected routes (Dashboard) require active login session
- Unauthorized users are redirected to the login page
- Sessions are cleared on logout to prevent reuse

---

## 🔑 Password Security Design

### Password Storage
- Passwords are hashed using:
  - **PBKDF2 + SHA256 (Werkzeug)**
- Each password is automatically **salted**
- Plain-text passwords are never stored or logged

### Password Policy
- Minimum password length enforced (8 characters)
- Password confirmation required during reset
- Server-side validation for all password changes

---

## 🔁 Password Reset Security

### Reset Flow
1. User submits registered email
2. Application generates a **cryptographically secure token**
3. Token expiry set to **1 hour**
4. Reset link sent via SMTP email
5. Token validated before password update
6. Token invalidated after successful reset

### Protection Measures
- Generic messages prevent account enumeration
- Expired or invalid tokens are rejected
- Reset tokens are stored securely in the database

---

## 🛡️ Threat Model & Protection

| Threat | Protection Implemented |
|------|------------------------|
| SQL Injection | Parameterized MySQL queries (`%s`) |
| Cross-Site Scripting (XSS) | Input validation & Jinja2 auto-escaping |
| Password Attacks | Strong hashing + salting |
| CSRF Attacks | Flask-WTF CSRF tokens |
| Session Hijacking | Secure cookies & session clearing |
| Account Enumeration | Generic forgot-password responses |

---

## 🔐 Session Security Design

- Flask session management used
- Session cleared on logout using `session.clear()`
- Secure cookie flags applied:
  - HttpOnly
  - SameSite = Lax
  - Secure (recommended for HTTPS)

---

## 🧪 Input Validation & Sanitization

- All form inputs validated server-side
- Required fields checked before database operations
- Length checks applied where needed
- No direct SQL string concatenation used

---

## ⚙️ Configuration & Secrets Management

- All sensitive data stored in `.env` file:
  - Database credentials
  - Secret key
  - SMTP credentials
- `.env` is excluded using `.gitignore`
- Different behavior for development and production via `DEV_MODE`

---

## 🚀 Secure Development Practices Followed

- Principle of Least Privilege
- Secure defaults
- Fail-safe authentication
- No sensitive data exposed in logs
- Defensive error handling

---

## 🔮 Future Security Enhancements

- Role-Based Access Control (Admin/User)
- Login rate-limiting
- Two-Factor Authentication (2FA)
- Email verification on registration
- Security audit logging

---

## ✅ Conclusion

This application demonstrates a **secure-by-design approach**
and covers essential **web application security controls**.

It is suitable for:
- Cybersecurity academic submission
- Internship portfolio
- Entry-level SOC / AppSec learning projects

---

**Author:** Trupti Lavate  
**Domain:** Cybersecurity & Secure Web Development
