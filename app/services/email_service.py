"""
Email service — sends emails via SMTP or prints to console in dev mode.
"""
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import current_app

logger = logging.getLogger(__name__)


def send_email(to_email, subject, html_body):
    """
    Send an HTML email.
    Falls back to console logging if MAIL_USERNAME is not configured.
    """
    mail_user = current_app.config.get('MAIL_USERNAME', '')
    if not mail_user:
        # Development / console mode
        logger.info(f"[EMAIL] To:{to_email} | Subject:{subject}\n{html_body}")
        print(f"\n{'='*60}\n[EMAIL] To: {to_email}\nSubject: {subject}\n{html_body}\n{'='*60}\n")
        return

    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = current_app.config['MAIL_DEFAULT_SENDER']
        msg['To'] = to_email
        msg.attach(MIMEText(html_body, 'html'))

        with smtplib.SMTP(current_app.config['MAIL_SERVER'],
                          current_app.config['MAIL_PORT']) as server:
            if current_app.config.get('MAIL_USE_TLS'):
                server.starttls()
            server.login(mail_user, current_app.config['MAIL_PASSWORD'])
            server.sendmail(msg['From'], [to_email], msg.as_string())
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")


def send_password_reset_email(to_email, reset_link):
    html = f"""
    <h2>Password Reset Request</h2>
    <p>Click the link below to reset your password. The link is valid for 1 hour.</p>
    <a href="{reset_link}" style="background:#4f46e5;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">
      Reset Password
    </a>
    <p>If you did not request this, please ignore this email.</p>
    """
    send_email(to_email, "Reset Your Password — Freelance Marketplace", html)


def send_verification_email(to_email, verify_link):
    html = f"""
    <h2>Verify Your Email</h2>
    <p>Click the link below to verify your email address.</p>
    <a href="{verify_link}" style="background:#10b981;color:#fff;padding:10px 20px;text-decoration:none;border-radius:5px;">
      Verify Email
    </a>
    """
    send_email(to_email, "Verify Your Email — Freelance Marketplace", html)
