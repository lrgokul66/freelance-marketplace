"""
Project model — DB operations for projects, project_skills, project_files, saved_projects.
"""
from database import execute_query


class ProjectModel:

    # ── Create / Edit / Delete ────────────────────────────────
    @staticmethod
    def create_project(client_id, data):
        project_id = execute_query(
            """INSERT INTO projects
               (client_id, title, category, description, budget_min, budget_max,
                experience_level, duration, deadline, status)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,'open')""",
            (client_id, data['title'], data['category'], data['description'],
             data['budget_min'], data['budget_max'], data['experience_level'],
             data.get('duration'), data.get('deadline') or None),
            fetch='none', commit=True
        )
        return project_id

    @staticmethod
    def update_project(project_id, data):
        execute_query(
            """UPDATE projects SET title=%s, category=%s, description=%s,
               budget_min=%s, budget_max=%s, experience_level=%s,
               duration=%s, deadline=%s WHERE id=%s""",
            (data['title'], data['category'], data['description'],
             data['budget_min'], data['budget_max'], data['experience_level'],
             data.get('duration'), data.get('deadline') or None, project_id),
            fetch='none', commit=True
        )

    @staticmethod
    def delete_project(project_id, client_id):
        execute_query(
            "DELETE FROM projects WHERE id=%s AND client_id=%s",
            (project_id, client_id), fetch='none', commit=True
        )

    @staticmethod
    def update_status(project_id, status, hired_freelancer_id=None):
        execute_query(
            "UPDATE projects SET status=%s, hired_freelancer_id=%s WHERE id=%s",
            (status, hired_freelancer_id, project_id),
            fetch='none', commit=True
        )

    # ── Fetch ─────────────────────────────────────────────────
    @staticmethod
    def get_by_id(project_id):
        return execute_query(
            """SELECT p.*, u.first_name, u.last_name,
                       u.first_name AS client_first, u.last_name AS client_last,
                       u.created_at AS client_joined,
                       cp.company, cp.avatar AS client_avatar, cp.location
               FROM projects p
               JOIN users u ON u.id=p.client_id
               LEFT JOIN client_profiles cp ON cp.user_id=p.client_id
               WHERE p.id=%s""",
            (project_id,), fetch='one'
        )

    @staticmethod
    def get_by_client(client_id):
        return execute_query(
            """SELECT p.*,
                      (SELECT COUNT(*) FROM proposals WHERE project_id=p.id) AS proposal_count
               FROM projects p
               WHERE p.client_id=%s
               ORDER BY p.created_at DESC""",
            (client_id,), fetch='all'
        )

    @staticmethod
    def increment_views(project_id):
        execute_query(
            "UPDATE projects SET views=views+1 WHERE id=%s",
            (project_id,), fetch='none', commit=True
        )

    # ── Project Skills ────────────────────────────────────────
    @staticmethod
    def set_project_skills(project_id, skill_ids):
        execute_query(
            "DELETE FROM project_skills WHERE project_id=%s",
            (project_id,), fetch='none', commit=True
        )
        for sid in skill_ids:
            execute_query(
                "INSERT IGNORE INTO project_skills (project_id, skill_id) VALUES (%s,%s)",
                (project_id, sid), fetch='none', commit=True
            )

    @staticmethod
    def get_project_skills(project_id):
        return execute_query(
            """SELECT s.id, s.name FROM skills s
               JOIN project_skills ps ON ps.skill_id=s.id
               WHERE ps.project_id=%s""",
            (project_id,), fetch='all'
        )

    # ── Project Files ─────────────────────────────────────────
    @staticmethod
    def add_file(project_id, filename, original_name):
        execute_query(
            "INSERT INTO project_files (project_id, filename, original_name) VALUES (%s,%s,%s)",
            (project_id, filename, original_name), fetch='none', commit=True
        )

    @staticmethod
    def get_files(project_id):
        return execute_query(
            "SELECT id, project_id, filename, filename AS file_path, original_name FROM project_files WHERE project_id=%s",
            (project_id,), fetch='all'
        )

    @staticmethod
    def delete_file(file_id, project_id):
        return execute_query(
            "SELECT filename FROM project_files WHERE id=%s AND project_id=%s",
            (file_id, project_id), fetch='one'
        )

    # ── Search / Browse ───────────────────────────────────────
    @staticmethod
    def search_projects(keyword='', category='', skill_id=None,
                        budget_min=None, budget_max=None,
                        experience_level='', duration='',
                        sort='latest', page=1, per_page=12):
        conditions = ["p.status='open'"]
        params = []

        if keyword:
            conditions.append("(p.title LIKE %s OR p.description LIKE %s)")
            k = f'%{keyword}%'
            params += [k, k]
        if category:
            conditions.append("p.category=%s")
            params.append(category)
        if skill_id:
            conditions.append(
                "p.id IN (SELECT project_id FROM project_skills WHERE skill_id=%s)"
            )
            params.append(skill_id)
        if budget_min is not None:
            conditions.append("p.budget_max >= %s")
            params.append(budget_min)
        if budget_max is not None:
            conditions.append("p.budget_min <= %s")
            params.append(budget_max)
        if experience_level:
            conditions.append("p.experience_level=%s")
            params.append(experience_level)
        if duration:
            conditions.append("p.duration=%s")
            params.append(duration)

        where = ' AND '.join(conditions)
        order = 'p.created_at DESC' if sort == 'latest' else 'p.views DESC'
        offset = (page - 1) * per_page

        rows = execute_query(
            f"""SELECT p.*, u.first_name, u.last_name, cp.avatar AS client_avatar,
                       (SELECT COUNT(*) FROM proposals WHERE project_id=p.id) AS proposal_count
                FROM projects p
                JOIN users u ON u.id=p.client_id
                LEFT JOIN client_profiles cp ON cp.user_id=p.client_id
                WHERE {where}
                ORDER BY {order}
                LIMIT %s OFFSET %s""",
            params + [per_page, offset], fetch='all'
        )
        total_row = execute_query(
            f"SELECT COUNT(*) AS total FROM projects p WHERE {where}",
            params, fetch='one'
        )
        return rows, (total_row['total'] if total_row else 0)

    @staticmethod
    def get_categories():
        rows = execute_query(
            "SELECT DISTINCT category FROM projects ORDER BY category",
            fetch='all'
        )
        return [r['category'] for r in rows] if rows else []

    # ── Saved Projects ────────────────────────────────────────
    @staticmethod
    def save_project(freelancer_id, project_id):
        execute_query(
            "INSERT IGNORE INTO saved_projects (freelancer_id, project_id) VALUES (%s,%s)",
            (freelancer_id, project_id), fetch='none', commit=True
        )

    @staticmethod
    def unsave_project(freelancer_id, project_id):
        execute_query(
            "DELETE FROM saved_projects WHERE freelancer_id=%s AND project_id=%s",
            (freelancer_id, project_id), fetch='none', commit=True
        )

    @staticmethod
    def is_saved(freelancer_id, project_id):
        row = execute_query(
            "SELECT id FROM saved_projects WHERE freelancer_id=%s AND project_id=%s",
            (freelancer_id, project_id), fetch='one'
        )
        return row is not None

    @staticmethod
    def get_saved_projects(freelancer_id):
        return execute_query(
            """SELECT p.*, u.first_name, u.last_name
               FROM saved_projects sp
               JOIN projects p ON p.id=sp.project_id
               JOIN users u ON u.id=p.client_id
               WHERE sp.freelancer_id=%s
               ORDER BY sp.saved_at DESC""",
            (freelancer_id,), fetch='all'
        )
