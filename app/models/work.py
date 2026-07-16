"""
Work Submission model.
"""
from database import execute_query


class WorkModel:

    @staticmethod
    def submit(project_id, freelancer_id, file_path, original_name, notes=''):
        return execute_query(
            """INSERT INTO work_submissions
               (project_id, freelancer_id, file_path, original_name, notes)
               VALUES (%s,%s,%s,%s,%s)""",
            (project_id, freelancer_id, file_path, original_name, notes),
            fetch='none', commit=True
        )

    @staticmethod
    def get_by_project(project_id):
        return execute_query(
            """SELECT ws.*, u.first_name, u.last_name
               FROM work_submissions ws
               JOIN users u ON u.id=ws.freelancer_id
               WHERE ws.project_id=%s
               ORDER BY ws.submitted_at DESC""",
            (project_id,), fetch='all'
        )

    @staticmethod
    def get_by_id(submission_id):
        return execute_query(
            "SELECT * FROM work_submissions WHERE id=%s",
            (submission_id,), fetch='one'
        )

    @staticmethod
    def review(submission_id, status, client_feedback):
        execute_query(
            """UPDATE work_submissions SET status=%s, client_feedback=%s,
               reviewed_at=NOW() WHERE id=%s""",
            (status, client_feedback, submission_id),
            fetch='none', commit=True
        )
