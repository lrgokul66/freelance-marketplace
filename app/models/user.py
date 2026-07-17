"""
User model — handles all DB operations for the users table
and related profile tables.
"""
from database import execute_query
from flask_bcrypt import generate_password_hash, check_password_hash


class UserModel:
    # ── Auth ──────────────────────────────────────────────────
    @staticmethod
    def create_user(email, password, role, first_name, last_name):
        pwd_hash = generate_password_hash(password).decode('utf-8')
        user_id = execute_query(
            """INSERT INTO users (email, password_hash, role, first_name, last_name)
               VALUES (%s, %s, %s, %s, %s)""",
            (email, pwd_hash, role, first_name, last_name),
            fetch='none', commit=True
        )
        # Create empty profile
        if role == 'client':
            execute_query(
                "INSERT INTO client_profiles (user_id) VALUES (%s)",
                (user_id,), fetch='none', commit=True
            )
        else:
            execute_query(
                "INSERT INTO freelancer_profiles (user_id) VALUES (%s)",
                (user_id,), fetch='none', commit=True
            )
        return user_id

    @staticmethod
    def get_by_email(email):
        return execute_query(
            "SELECT * FROM users WHERE email=%s AND is_active=1",
            (email,), fetch='one'
        )

    @staticmethod
    def get_by_id(user_id):
        return execute_query(
            "SELECT * FROM users WHERE id=%s AND is_active=1",
            (user_id,), fetch='one'
        )

    @staticmethod
    def verify_password(stored_hash, password):
        return check_password_hash(stored_hash, password)

    @staticmethod
    def update_password(user_id, new_password):
        pwd_hash = generate_password_hash(new_password).decode('utf-8')
        execute_query(
            "UPDATE users SET password_hash=%s WHERE id=%s",
            (pwd_hash, user_id), fetch='none', commit=True
        )

    @staticmethod
    def mark_verified(user_id):
        execute_query(
            "UPDATE users SET is_verified=1 WHERE id=%s",
            (user_id,), fetch='none', commit=True
        )

    @staticmethod
    def email_exists(email):
        row = execute_query(
            "SELECT id FROM users WHERE email=%s",
            (email,), fetch='one'
        )
        return row is not None

    # ── Client Profile ────────────────────────────────────────
    @staticmethod
    def get_client_profile(user_id):
        return execute_query(
            """SELECT u.*, cp.*,
                      u.first_name, u.last_name, u.email, u.created_at AS member_since
               FROM users u
               JOIN client_profiles cp ON cp.user_id = u.id
               WHERE u.id=%s""",
            (user_id,), fetch='one'
        )

    @staticmethod
    def update_client_profile(user_id, data):
        execute_query(
            """UPDATE client_profiles
               SET company=%s, website=%s, location=%s, phone=%s, description=%s
               WHERE user_id=%s""",
            (data.get('company'), data.get('website'), data.get('location'),
             data.get('phone'), data.get('description'), user_id),
            fetch='none', commit=True
        )
        execute_query(
            "UPDATE users SET first_name=%s, last_name=%s WHERE id=%s",
            (data.get('first_name'), data.get('last_name'), user_id),
            fetch='none', commit=True
        )

    @staticmethod
    def update_client_avatar(user_id, filename):
        execute_query(
            "UPDATE client_profiles SET avatar=%s WHERE user_id=%s",
            (filename, user_id), fetch='none', commit=True
        )

    # ── Freelancer Profile ────────────────────────────────────
    @staticmethod
    def get_freelancer_profile(user_id):
        return execute_query(
            """SELECT u.*, fp.*,
                      u.first_name, u.last_name, u.email, u.created_at AS member_since
               FROM users u
               JOIN freelancer_profiles fp ON fp.user_id = u.id
               WHERE u.id=%s""",
            (user_id,), fetch='one'
        )

    @staticmethod
    def update_freelancer_profile(user_id, data):
        execute_query(
            """UPDATE freelancer_profiles
               SET headline=%s, bio=%s, hourly_rate=%s, availability=%s, languages=%s, location=%s, experience_years=%s
               WHERE user_id=%s""",
            (data.get('headline'), data.get('bio'), data.get('hourly_rate'),
             data.get('availability'), data.get('languages'), data.get('location'),
             data.get('experience_years'), user_id),
            fetch='none', commit=True
        )
        execute_query(
            "UPDATE users SET first_name=%s, last_name=%s WHERE id=%s",
            (data.get('first_name'), data.get('last_name'), user_id),
            fetch='none', commit=True
        )

    @staticmethod
    def update_freelancer_avatar(user_id, filename):
        execute_query(
            "UPDATE freelancer_profiles SET avatar=%s WHERE user_id=%s",
            (filename, user_id), fetch='none', commit=True
        )

    @staticmethod
    def update_freelancer_resume(user_id, filename):
        execute_query(
            "UPDATE freelancer_profiles SET resume=%s WHERE user_id=%s",
            (filename, user_id), fetch='none', commit=True
        )

    # ── Skills ────────────────────────────────────────────────
    @staticmethod
    def get_all_skills():
        return execute_query("SELECT * FROM skills ORDER BY name", fetch='all')

    @staticmethod
    def get_freelancer_skills(freelancer_profile_id):
        return execute_query(
            """SELECT s.id, s.name FROM skills s
               JOIN freelancer_skills fs ON fs.skill_id = s.id
               WHERE fs.freelancer_id=%s""",
            (freelancer_profile_id,), fetch='all'
        )

    @staticmethod
    def set_freelancer_skills(freelancer_profile_id, skill_ids):
        execute_query(
            "DELETE FROM freelancer_skills WHERE freelancer_id=%s",
            (freelancer_profile_id,), fetch='none', commit=True
        )
        for sid in skill_ids:
            execute_query(
                "INSERT IGNORE INTO freelancer_skills (freelancer_id, skill_id) VALUES (%s,%s)",
                (freelancer_profile_id, sid), fetch='none', commit=True
            )

    @staticmethod
    def get_or_create_skill(name):
        name = name.strip()
        row = execute_query("SELECT id FROM skills WHERE name=%s", (name,), fetch='one')
        if row:
            return row['id']
        return execute_query(
            "INSERT INTO skills (name) VALUES (%s)",
            (name,), fetch='none', commit=True
        )

    # ── Portfolio, Education, Experience, Certifications ──────
    @staticmethod
    def get_portfolio(freelancer_profile_id):
        return execute_query(
            "SELECT * FROM portfolio WHERE freelancer_id=%s ORDER BY id DESC",
            (freelancer_profile_id,), fetch='all'
        )

    @staticmethod
    def add_portfolio(freelancer_profile_id, title, description, image, link):
        return execute_query(
            "INSERT INTO portfolio (freelancer_id,title,description,image,link) VALUES (%s,%s,%s,%s,%s)",
            (freelancer_profile_id, title, description, image, link),
            fetch='none', commit=True
        )

    @staticmethod
    def delete_portfolio(portfolio_id, freelancer_profile_id):
        execute_query(
            "DELETE FROM portfolio WHERE id=%s AND freelancer_id=%s",
            (portfolio_id, freelancer_profile_id), fetch='none', commit=True
        )

    @staticmethod
    def get_education(freelancer_profile_id):
        return execute_query(
            "SELECT * FROM education WHERE freelancer_id=%s ORDER BY year DESC",
            (freelancer_profile_id,), fetch='all'
        )

    @staticmethod
    def add_education(freelancer_profile_id, degree, institution, year, description):
        execute_query(
            "INSERT INTO education (freelancer_id,degree,institution,year,description) VALUES (%s,%s,%s,%s,%s)",
            (freelancer_profile_id, degree, institution, year or None, description),
            fetch='none', commit=True
        )

    @staticmethod
    def delete_education(edu_id, freelancer_profile_id):
        execute_query(
            "DELETE FROM education WHERE id=%s AND freelancer_id=%s",
            (edu_id, freelancer_profile_id), fetch='none', commit=True
        )

    @staticmethod
    def get_experience(freelancer_profile_id):
        return execute_query(
            "SELECT * FROM experience WHERE freelancer_id=%s ORDER BY id DESC",
            (freelancer_profile_id,), fetch='all'
        )

    @staticmethod
    def add_experience(freelancer_profile_id, title, company, years, description):
        execute_query(
            "INSERT INTO experience (freelancer_id,title,company,years,description) VALUES (%s,%s,%s,%s,%s)",
            (freelancer_profile_id, title, company, years, description),
            fetch='none', commit=True
        )

    @staticmethod
    def delete_experience(exp_id, freelancer_profile_id):
        execute_query(
            "DELETE FROM experience WHERE id=%s AND freelancer_id=%s",
            (exp_id, freelancer_profile_id), fetch='none', commit=True
        )

    @staticmethod
    def get_certifications(freelancer_profile_id):
        return execute_query(
            "SELECT * FROM certifications WHERE freelancer_id=%s ORDER BY year DESC",
            (freelancer_profile_id,), fetch='all'
        )

    @staticmethod
    def add_certification(freelancer_profile_id, name, issuer, year):
        execute_query(
            "INSERT INTO certifications (freelancer_id,name,issuer,year) VALUES (%s,%s,%s,%s)",
            (freelancer_profile_id, name, issuer, year or None),
            fetch='none', commit=True
        )

    @staticmethod
    def delete_certification(cert_id, freelancer_profile_id):
        execute_query(
            "DELETE FROM certifications WHERE id=%s AND freelancer_id=%s",
            (cert_id, freelancer_profile_id), fetch='none', commit=True
        )

    # ── Average rating ────────────────────────────────────────
    @staticmethod
    def get_avg_rating(user_id):
        row = execute_query(
            "SELECT ROUND(AVG(rating),1) AS avg_rating, COUNT(*) AS total FROM reviews WHERE reviewee_id=%s",
            (user_id,), fetch='one'
        )
        return row or {'avg_rating': 0, 'total': 0}

    # ── Account Deletion ──────────────────────────────────────
    @staticmethod
    def delete_account(user_id):
        """
        Permanently delete all user data.
        Foreign keys with ON DELETE CASCADE handle child records automatically.
        """
        execute_query(
            "DELETE FROM users WHERE id=%s",
            (user_id,), fetch='none', commit=True
        )

    # ── Search Freelancers ────────────────────────────────────
    @staticmethod
    def search_freelancers(keyword='', skill_id=None, availability=None, page=1, per_page=12):
        conditions = ["u.role='freelancer'", "u.is_active=1"]
        params = []
        if keyword:
            conditions.append("(u.first_name LIKE %s OR u.last_name LIKE %s OR fp.headline LIKE %s OR fp.bio LIKE %s)")
            k = f'%{keyword}%'
            params += [k, k, k, k]
        if skill_id:
            conditions.append(
                "fp.id IN (SELECT freelancer_id FROM freelancer_skills WHERE skill_id=%s)"
            )
            params.append(skill_id)
        if availability:
            conditions.append("fp.availability=%s")
            params.append(availability)

        where = ' AND '.join(conditions)
        offset = (page - 1) * per_page
        rows = execute_query(
            f"""SELECT u.id, u.first_name, u.last_name, u.created_at,
                       fp.headline, fp.hourly_rate, fp.availability, fp.avatar,
                       ROUND(AVG(r.rating),1) AS avg_rating, COUNT(r.id) AS review_count
                FROM users u
                JOIN freelancer_profiles fp ON fp.user_id=u.id
                LEFT JOIN reviews r ON r.reviewee_id=u.id
                WHERE {where}
                GROUP BY u.id
                ORDER BY avg_rating DESC
                LIMIT %s OFFSET %s""",
            params + [per_page, offset], fetch='all'
        )
        total_row = execute_query(
            f"SELECT COUNT(DISTINCT u.id) AS total FROM users u JOIN freelancer_profiles fp ON fp.user_id=u.id WHERE {where}",
            params, fetch='one'
        )
        return rows, (total_row['total'] if total_row else 0)
