"""
Proposal model — DB operations for proposals and proposal_files.
"""
from database import execute_query


class ProposalModel:

    @staticmethod
    def create(project_id, freelancer_id, data):
        proposal_id = execute_query(
            """INSERT INTO proposals
               (project_id, freelancer_id, cover_letter, bid_amount, delivery_days, portfolio_links)
               VALUES (%s,%s,%s,%s,%s,%s)""",
            (project_id, freelancer_id, data['cover_letter'],
             data['bid_amount'], data['delivery_days'],
             data.get('portfolio_links', '')),
            fetch='none', commit=True
        )
        return proposal_id

    @staticmethod
    def update(proposal_id, freelancer_id, data):
        execute_query(
            """UPDATE proposals SET cover_letter=%s, bid_amount=%s,
               delivery_days=%s, portfolio_links=%s
               WHERE id=%s AND freelancer_id=%s""",
            (data['cover_letter'], data['bid_amount'],
             data['delivery_days'], data.get('portfolio_links', ''),
             proposal_id, freelancer_id),
            fetch='none', commit=True
        )

    @staticmethod
    def update_status(proposal_id, status, client_note=None):
        execute_query(
            "UPDATE proposals SET status=%s, client_note=%s WHERE id=%s",
            (status, client_note, proposal_id),
            fetch='none', commit=True
        )

    @staticmethod
    def withdraw(proposal_id, freelancer_id):
        execute_query(
            "UPDATE proposals SET status='withdrawn' WHERE id=%s AND freelancer_id=%s",
            (proposal_id, freelancer_id), fetch='none', commit=True
        )

    @staticmethod
    def delete(proposal_id, freelancer_id):
        execute_query(
            "DELETE FROM proposals WHERE id=%s AND freelancer_id=%s AND status='pending'",
            (proposal_id, freelancer_id), fetch='none', commit=True
        )

    @staticmethod
    def get_by_id(proposal_id):
        return execute_query(
            """SELECT pr.*, p.title AS project_title, p.client_id,
                      u.first_name, u.last_name, fp.headline, fp.avatar, fp.hourly_rate,
                      ROUND(AVG(r.rating),1) AS avg_rating
               FROM proposals pr
               JOIN projects p ON p.id=pr.project_id
               JOIN users u ON u.id=pr.freelancer_id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=pr.freelancer_id
               LEFT JOIN reviews r ON r.reviewee_id=pr.freelancer_id
               WHERE pr.id=%s
               GROUP BY pr.id""",
            (proposal_id,), fetch='one'
        )

    @staticmethod
    def get_by_project(project_id):
        return execute_query(
            """SELECT pr.*, u.first_name AS freelancer_first, u.last_name AS freelancer_last,
                      fp.headline, fp.avatar, fp.hourly_rate, fp.availability,
                      ROUND(AVG(r.rating),1) AS avg_rating,
                      COUNT(DISTINCT r.id) AS review_count,
                      (SELECT COUNT(*) FROM proposals WHERE freelancer_id=pr.freelancer_id
                       AND status='accepted') AS completed_projects
               FROM proposals pr
               JOIN users u ON u.id=pr.freelancer_id
               LEFT JOIN freelancer_profiles fp ON fp.user_id=pr.freelancer_id
               LEFT JOIN reviews r ON r.reviewee_id=pr.freelancer_id
               WHERE pr.project_id=%s
               GROUP BY pr.id
               ORDER BY pr.created_at DESC""",
            (project_id,), fetch='all'
        )

    @staticmethod
    def get_by_freelancer(freelancer_id, page=1, per_page=10):
        offset = (page - 1) * per_page
        rows = execute_query(
            """SELECT pr.*, p.title AS project_title, p.status AS project_status, p.client_id,
                      u.first_name AS client_first, u.last_name AS client_last,
                      cp.company
               FROM proposals pr
               JOIN projects p ON p.id=pr.project_id
               JOIN users u ON u.id=p.client_id
               LEFT JOIN client_profiles cp ON cp.user_id=p.client_id
               WHERE pr.freelancer_id=%s
               ORDER BY pr.created_at DESC
               LIMIT %s OFFSET %s""",
            (freelancer_id, per_page, offset), fetch='all'
        )
        total_row = execute_query(
            "SELECT COUNT(*) AS total FROM proposals WHERE freelancer_id=%s",
            (freelancer_id,), fetch='one'
        )
        return rows, (total_row['total'] if total_row else 0)

    @staticmethod
    def already_proposed(project_id, freelancer_id):
        row = execute_query(
            "SELECT id FROM proposals WHERE project_id=%s AND freelancer_id=%s",
            (project_id, freelancer_id), fetch='one'
        )
        return row

    # ── Files ─────────────────────────────────────────────────
    @staticmethod
    def add_file(proposal_id, filename, original_name):
        execute_query(
            "INSERT INTO proposal_files (proposal_id,filename,original_name) VALUES (%s,%s,%s)",
            (proposal_id, filename, original_name), fetch='none', commit=True
        )

    @staticmethod
    def get_files(proposal_id):
        return execute_query(
            "SELECT id, proposal_id, filename, filename AS file_path, original_name FROM proposal_files WHERE proposal_id=%s",
            (proposal_id,), fetch='all'
        )
