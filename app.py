from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from config import db_config
import os
from dotenv import load_dotenv
import secrets
from datetime import datetime, timedelta
from flask_wtf.csrf import CSRFProtect
import smtplib
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
csrf = CSRFProtect(app)
# DEV_MODE controls whether dev-only conveniences (like clickable reset links) are shown
DEV_MODE = os.getenv('DEV_MODE', 'True').lower() in ('1', 'true', 'yes')
app.config['DEV_MODE'] = DEV_MODE

def get_db_connection():
    return mysql.connector.connect(**db_config)


def send_reset_email(to_email: str, reset_url: str) -> bool:
    """Send reset URL to user via SMTP. Returns True on success."""
    smtp_host = os.getenv('SMTP_HOST')
    smtp_port = int(os.getenv('SMTP_PORT', '587'))
    smtp_user = os.getenv('SMTP_USER')
    smtp_password = os.getenv('SMTP_PASSWORD')
    smtp_from = os.getenv('SMTP_FROM')
    use_tls = os.getenv('SMTP_USE_TLS', 'True').lower() in ('1', 'true', 'yes')

    if not smtp_host or not smtp_from:
        app.logger.warning('SMTP not configured; skipping email send')
        return False

    # Render email templates (plain + HTML)
    try:
        html_body = render_template('email/reset_password.html', reset_url=reset_url)
    except Exception:
        html_body = f"<p>Click this link to reset your password: <a href='{reset_url}'>{reset_url}</a></p>"

    text_body = f"Click this link to reset your password: {reset_url}\n\nIf you did not request this, ignore."

    msg = EmailMessage()
    msg['Subject'] = 'Reset your password'
    msg['From'] = smtp_from
    msg['To'] = to_email
    msg.set_content(text_body)
    msg.add_alternative(html_body, subtype='html')

    try:
        if use_tls:
            server = smtplib.SMTP(smtp_host, smtp_port, timeout=10)
            server.starttls()
        else:
            server = smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=10)

        if smtp_user and smtp_password:
            server.login(smtp_user, smtp_password)

        server.send_message(msg)
        server.quit()
        app.logger.info(f'Reset email sent to {to_email}')
        return True
    except Exception as e:
        app.logger.error(f'Failed to send reset email: {e}')
        return False

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            if not all([username, email, password]):
                flash("All fields are required", "error")
                return redirect(url_for("register"))

            if len(password) < 8:
                flash("Password must be at least 8 characters long", "error")
                return redirect(url_for("register"))

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)

            # 🔍 Duplicate check
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            existing_user = cursor.fetchone()

            if existing_user:
                flash("Username or Email already exists", "error")
                cursor.close()
                db.close()
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(password)

            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, hashed_password)
            )
            db.commit()

            cursor.close()
            db.close()

            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("register"))

    return render_template("register.html", dev_mode=app.config.get('DEV_MODE', False))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")

            if not all([username, password]):
                flash("All fields are required", "error")
                return redirect(url_for("login"))

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
            cursor.close()
            db.close()

            if user and check_password_hash(user["password"], password):
                session["user"] = username
                session["user_id"] = user["id"]
                flash("Login successful", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password", "error")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")

    return render_template("login.html", dev_mode=app.config.get('DEV_MODE', False))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        flash("Please login first", "error")
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=session["user"], dev_mode=app.config.get('DEV_MODE', False))

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("login"))

@app.route("/forgot", methods=["GET", "POST"])
def forgot():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            
            if not email:
                flash("Email is required", "error")
                return redirect(url_for("forgot"))

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            user = cursor.fetchone()

            if not user:
                # Don't reveal if email exists
                flash("If that email exists, you will receive a password reset link", "info")
                cursor.close()
                db.close()
                return redirect(url_for("login"))

            # Generate secure reset token
            reset_token = secrets.token_urlsafe(32)
            token_expiry = datetime.now() + timedelta(hours=1)

            cursor.execute(
                "UPDATE users SET reset_token=%s, reset_token_expiry=%s WHERE email=%s",
                (reset_token, token_expiry, email)
            )
            db.commit()
            cursor.close()
            db.close()

            # Send email with reset link if SMTP configured; otherwise keep dev behavior
            reset_url = url_for('reset_password', token=reset_token, _external=True)
            sent = send_reset_email(email, reset_url)
            app.logger.info(f"Password reset token for {email}: {reset_token}")

            if sent:
                flash('If that email exists, you will receive a password reset link shortly.', 'info')
            else:
                # fallback for development: show clickable link only when email not sent
                flash(f'Password reset link (dev): <a href="{reset_url}">Reset your password</a>', 'info')

            return redirect(url_for("login"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("forgot"))

    return render_template("forgot.html", dev_mode=app.config.get('DEV_MODE', False))

@app.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    if request.method == "POST":
        try:
            new_password = request.form.get("password", "")
            confirm_password = request.form.get("confirm_password", "")

            if not new_password or not confirm_password:
                flash("All fields are required", "error")
                return redirect(url_for("reset_password", token=token))

            if len(new_password) < 8:
                flash("Password must be at least 8 characters long", "error")
                return redirect(url_for("reset_password", token=token))

            if new_password != confirm_password:
                flash("Passwords do not match", "error")
                return redirect(url_for("reset_password", token=token))

            db = get_db_connection()
            cursor = db.cursor(dictionary=True)
            cursor.execute(
                "SELECT * FROM users WHERE reset_token=%s AND reset_token_expiry > %s",
                (token, datetime.now())
            )
            user = cursor.fetchone()

            if not user:
                flash("Invalid or expired reset token", "error")
                cursor.close()
                db.close()
                return redirect(url_for("login"))

            hashed_password = generate_password_hash(new_password)
            cursor.execute(
                "UPDATE users SET password=%s, reset_token=NULL, reset_token_expiry=NULL WHERE id=%s",
                (hashed_password, user["id"])
            )
            db.commit()
            cursor.close()
            db.close()

            flash("Password reset successful! Please login with your new password.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for("reset_password", token=token))

    return render_template("reset.html", token=token, dev_mode=app.config.get('DEV_MODE', False))

if __name__ == "__main__":
    app.run(debug=True)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
