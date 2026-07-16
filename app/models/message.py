"""
Message model — private chat between client and freelancer per project.
"""
from database import execute_query


class MessageModel:

    @staticmethod
    def send(sender_id, receiver_id, project_id, content=None, file_path=None, file_name=None):
        return execute_query(
            """INSERT INTO messages (sender_id, receiver_id, project_id, content, file_path, file_name)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (sender_id, receiver_id, project_id, content, file_path, file_name),
            fetch='none', commit=True
        )

    @staticmethod
    def get_conversation(project_id, user1_id, user2_id, limit=100):
        return execute_query(
            """SELECT m.*, u.first_name, u.last_name,
                      COALESCE(cp.avatar, fp.avatar) AS sender_avatar
               FROM messages m
               JOIN users u ON u.id=m.sender_id
               LEFT JOIN client_profiles cp ON cp.user_id=m.sender_id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=m.sender_id
               WHERE m.project_id=%s
                 AND ((m.sender_id=%s AND m.receiver_id=%s)
                       OR (m.sender_id=%s AND m.receiver_id=%s))
               ORDER BY m.created_at ASC
               LIMIT %s""",
            (project_id, user1_id, user2_id, user2_id, user1_id, limit),
            fetch='all'
        )

    @staticmethod
    def mark_read(project_id, receiver_id):
        execute_query(
            "UPDATE messages SET is_read=1 WHERE project_id=%s AND receiver_id=%s AND is_read=0",
            (project_id, receiver_id), fetch='none', commit=True
        )

    @staticmethod
    def get_new_messages_since(project_id, user1_id, user2_id, last_id):
        return execute_query(
            """SELECT m.*, u.first_name, u.last_name,
                      COALESCE(cp.avatar, fp.avatar) AS sender_avatar
               FROM messages m
               JOIN users u ON u.id=m.sender_id
               LEFT JOIN client_profiles cp ON cp.user_id=m.sender_id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=m.sender_id
               WHERE m.project_id=%s
                 AND ((m.sender_id=%s AND m.receiver_id=%s)
                       OR (m.sender_id=%s AND m.receiver_id=%s))
                 AND m.id > %s
               ORDER BY m.created_at ASC""",
            (project_id, user1_id, user2_id, user2_id, user1_id, last_id),
            fetch='all'
        )

    @staticmethod
    def get_conversations_for_user(user_id):
        """Get list of unique conversations (project+other_user) for a user."""
        return execute_query(
            """SELECT
                  m.project_id,
                  p.title AS project_title,
                  IF(m.sender_id=%s, m.receiver_id, m.sender_id) AS other_user_id,
                  u.first_name AS other_first, u.last_name AS other_last,
                  COALESCE(cp.avatar, fp.avatar) AS other_avatar,
                  MAX(m.created_at) AS last_time,
                  SUM(m.is_read=0 AND m.receiver_id=%s) AS unread_count,
                  (SELECT content FROM messages m2
                   WHERE m2.project_id=m.project_id
                     AND ((m2.sender_id=%s AND m2.receiver_id=IF(m.sender_id=%s, m.receiver_id, m.sender_id))
                           OR (m2.sender_id=IF(m.sender_id=%s, m.receiver_id, m.sender_id) AND m2.receiver_id=%s))
                   ORDER BY m2.created_at DESC LIMIT 1) AS last_message
               FROM messages m
               JOIN projects p ON p.id=m.project_id
               JOIN users u ON u.id=IF(m.sender_id=%s, m.receiver_id, m.sender_id)
               LEFT JOIN client_profiles cp ON cp.user_id=u.id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=u.id
               WHERE m.sender_id=%s OR m.receiver_id=%s
               GROUP BY m.project_id, other_user_id
               ORDER BY last_time DESC""",
            (user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id, user_id),
            fetch='all'
        )

    @staticmethod
    def get_unread_count(user_id):
        row = execute_query(
            "SELECT COUNT(*) AS cnt FROM messages WHERE receiver_id=%s AND is_read=0",
            (user_id,), fetch='one'
        )
        return row['cnt'] if row else 0
