"""
Authentication Blueprint — register, login, logout, forgot/reset password,
email verification, change password, account deletion.
"""
import functools
from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, current_app)
from app.models.user import UserModel
from app.services.token_service import generate_token, verify_token
from app.services.email_service import send_password_reset_email, send_verification_email

auth_bp = Blueprint('auth', __name__)

# ── Decorators ────────────────────────────────────────────────

def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


def role_required(role):
    def decorator(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            if 'user_id' not in session:
                flash('Please log in.', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('role') != role:
                flash('Access denied.', 'danger')
                return redirect(url_for('main.home'))
            return f(*args, **kwargs)
        return decorated
    return decorator


# ── Register ─────────────────────────────────────────────────
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return _dashboard_redirect()

    if request.method == 'POST':
        first_name  = request.form.get('first_name', '').strip()
        last_name   = request.form.get('last_name', '').strip()
        email       = request.form.get('email', '').strip().lower()
        password    = request.form.get('password', '')
        confirm_pwd = request.form.get('confirm_password', '')
        role        = request.form.get('role', '')

        # Validation
        errors = []
        if not all([first_name, last_name, email, password, role]):
            errors.append("All fields are required.")
        if role not in ('client', 'freelancer'):
            errors.append("Invalid role selected.")
        if len(password) < 8:
            errors.append("Password must be at least 8 characters.")
        if password != confirm_pwd:
            errors.append("Passwords do not match.")
        if UserModel.email_exists(email):
            errors.append("This email is already registered.")

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('auth/register.html',
                                   form=request.form)

        try:
            user_id = UserModel.create_user(email, password, role, first_name, last_name)
            # Send verification email
            token = generate_token(user_id, salt='email-verify')
            verify_link = url_for('auth.verify_email', token=token, _external=True)
            send_verification_email(email, verify_link)

            flash('Registration successful! Please check your email (or console) to verify.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as ex:
            current_app.logger.error(f"Register error: {ex}")
            flash('Registration failed. Please try again.', 'danger')

    return render_template('auth/register.html', form={})


# ── Email Verification ────────────────────────────────────────
@auth_bp.route('/verify-email/<token>')
def verify_email(token):
    user_id = verify_token(token, salt='email-verify', max_age=86400)
    if user_id is None:
        flash('Invalid or expired verification link.', 'danger')
        return redirect(url_for('auth.login'))
    UserModel.mark_verified(user_id)
    flash('Email verified! You can now log in.', 'success')
    return redirect(url_for('auth.login'))


# ── Login ─────────────────────────────────────────────────────
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return _dashboard_redirect()

    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = UserModel.get_by_email(email)
        if not user or not UserModel.verify_password(user['password_hash'], password):
            flash('Invalid email or password.', 'danger')
            return render_template('auth/login.html')

        # Build session
        session.clear()
        session['user_id']    = user['id']
        session['role']       = user['role']
        session['first_name'] = user['first_name']
        session['last_name']  = user['last_name']
        session['email']      = user['email']

        flash(f"Welcome back, {user['first_name']}!", 'success')
        next_page = request.args.get('next')
        return redirect(next_page or _dashboard_url(user['role']))

    return render_template('auth/login.html')


# ── Logout ────────────────────────────────────────────────────
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


# ── Forgot Password ───────────────────────────────────────────
@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user  = UserModel.get_by_email(email)
        # Always show same message to prevent email enumeration
        flash('If that email exists, a reset link has been sent (check console in dev).', 'info')
        if user:
            token = generate_token(user['id'], salt='password-reset')
            reset_link = url_for('auth.reset_password', token=token, _external=True)
            send_password_reset_email(email, reset_link)
        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


# ── Reset Password ────────────────────────────────────────────
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user_id = verify_token(token, salt='password-reset', max_age=3600)
    if user_id is None:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password    = request.form.get('password', '')
        confirm_pwd = request.form.get('confirm_password', '')
        if len(password) < 8:
            flash('Password must be at least 8 characters.', 'danger')
            return render_template('auth/reset_password.html', token=token)
        if password != confirm_pwd:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/reset_password.html', token=token)

        UserModel.update_password(user_id, password)
        flash('Password updated. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)


# ── Change Password (logged-in) ───────────────────────────────
@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    current = request.form.get('current_password', '')
    new_pwd = request.form.get('new_password', '')
    confirm = request.form.get('confirm_password', '')

    user = UserModel.get_by_id(session['user_id'])
    if not UserModel.verify_password(user['password_hash'], current):
        flash('Current password is incorrect.', 'danger')
    elif len(new_pwd) < 8:
        flash('New password must be at least 8 characters.', 'danger')
    elif new_pwd != confirm:
        flash('Passwords do not match.', 'danger')
    else:
        UserModel.update_password(session['user_id'], new_pwd)
        flash('Password changed successfully.', 'success')

    role = session.get('role')
    return redirect(url_for(f'{role}.edit_profile'))


# ── Delete Account ────────────────────────────────────────────
@auth_bp.route('/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'GET':
        return render_template('auth/delete_account.html')
    password    = request.form.get('confirm_password', '')
    typed_word  = request.form.get('delete_confirm', '').strip()
    user_id     = session['user_id']

    if typed_word != 'DELETE':
        flash('You must type DELETE to confirm.', 'danger')
        return redirect(url_for(f"{session['role']}.edit_profile"))

    user = UserModel.get_by_id(user_id)
    if not UserModel.verify_password(user['password_hash'], password):
        flash('Incorrect password. Account not deleted.', 'danger')
        return redirect(url_for(f"{session['role']}.edit_profile"))

    try:
        UserModel.delete_account(user_id)
        session.clear()
        flash('Your account has been permanently deleted.', 'success')
        return redirect(url_for('auth.login'))
    except Exception as ex:
        current_app.logger.error(f"Account deletion error: {ex}")
        flash('An error occurred. Please try again.', 'danger')
        return redirect(url_for(f"{session.get('role', 'auth')}.edit_profile"))


# ── Helpers ───────────────────────────────────────────────────
def _dashboard_url(role):
    return url_for('client.dashboard') if role == 'client' else url_for('freelancer.dashboard')


def _dashboard_redirect():
    role = session.get('role', 'client')
    return redirect(_dashboard_url(role))
