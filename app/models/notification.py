"""
Notification model.
"""
from database import execute_query


class NotificationModel:

    @staticmethod
    def create(user_id, type_, title, message, link=''):
        execute_query(
            """INSERT INTO notifications (user_id, type, title, message, link)
               VALUES (%s,%s,%s,%s,%s)""",
            (user_id, type_, title, message, link),
            fetch='none', commit=True
        )

    @staticmethod
    def get_for_user(user_id, limit=50):
        return execute_query(
            """SELECT * FROM notifications WHERE user_id=%s
               ORDER BY created_at DESC LIMIT %s""",
            (user_id, limit), fetch='all'
        )

    @staticmethod
    def get_unread_count(user_id):
        row = execute_query(
            "SELECT COUNT(*) AS cnt FROM notifications WHERE user_id=%s AND is_read=0",
            (user_id,), fetch='one'
        )
        return row['cnt'] if row else 0

    @staticmethod
    def mark_read(notification_id, user_id):
        execute_query(
            "UPDATE notifications SET is_read=1 WHERE id=%s AND user_id=%s",
            (notification_id, user_id), fetch='none', commit=True
        )

    @staticmethod
    def mark_all_read(user_id):
        execute_query(
            "UPDATE notifications SET is_read=1 WHERE user_id=%s",
            (user_id,), fetch='none', commit=True
        )
