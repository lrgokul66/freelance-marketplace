"""
Notifications Blueprint — list, mark-read, mark-all-read, AJAX unread count.
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, jsonify)
from app.routes.auth import login_required
from app.models.notification import NotificationModel

notifications_bp = Blueprint('notifications', __name__)


@notifications_bp.route('/')
@login_required
def list_notifications():
    notifications = NotificationModel.get_for_user(session['user_id'])
    return render_template('notifications/list.html', notifications=notifications)


@notifications_bp.route('/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_read(notification_id):
    NotificationModel.mark_read(notification_id, session['user_id'])
    return redirect(request.referrer or url_for('notifications.list_notifications'))


@notifications_bp.route('/read-all', methods=['POST'])
@login_required
def mark_all_read():
    NotificationModel.mark_all_read(session['user_id'])
    return redirect(url_for('notifications.list_notifications'))


@notifications_bp.route('/count')
@login_required
def unread_count():
    count = NotificationModel.get_unread_count(session['user_id'])
    return jsonify(count=count)
