"""
Review model — 5-star ratings and comments.
"""
from database import execute_query


class ReviewModel:

    @staticmethod
    def create(project_id, reviewer_id, reviewee_id, rating, comment):
        return execute_query(
            """INSERT INTO reviews (project_id, reviewer_id, reviewee_id, rating, comment)
               VALUES (%s,%s,%s,%s,%s)""",
            (project_id, reviewer_id, reviewee_id, rating, comment),
            fetch='none', commit=True
        )

    @staticmethod
    def already_reviewed(project_id, reviewer_id):
        row = execute_query(
            "SELECT id FROM reviews WHERE project_id=%s AND reviewer_id=%s",
            (project_id, reviewer_id), fetch='one'
        )
        return row is not None

    @staticmethod
    def get_for_user(user_id, page=1, per_page=10):
        offset = (page - 1) * per_page
        rows = execute_query(
            """SELECT r.*, u.first_name, u.last_name,
                      COALESCE(cp.avatar, fp.avatar) AS reviewer_avatar,
                      p.title AS project_title
               FROM reviews r
               JOIN users u ON u.id=r.reviewer_id
               LEFT JOIN client_profiles cp ON cp.user_id=r.reviewer_id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=r.reviewer_id
               JOIN projects p ON p.id=r.project_id
               WHERE r.reviewee_id=%s
               ORDER BY r.created_at DESC
               LIMIT %s OFFSET %s""",
            (user_id, per_page, offset), fetch='all'
        )
        total_row = execute_query(
            "SELECT COUNT(*) AS total FROM reviews WHERE reviewee_id=%s",
            (user_id,), fetch='one'
        )
        return rows, (total_row['total'] if total_row else 0)

    @staticmethod
    def get_for_project(project_id):
        return execute_query(
            """SELECT r.*, u.first_name, u.last_name
               FROM reviews r JOIN users u ON u.id=r.reviewer_id
               WHERE r.project_id=%s""",
            (project_id,), fetch='all'
        )
