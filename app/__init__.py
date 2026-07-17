"""
Freelance Marketplace — Flask Application Factory
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, render_template, send_from_directory
from config import get_config
from database import init_db


def create_app():
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static',
    )

    # ── Load configuration ──────────────────────────────────
    app.config.from_object(get_config())

    # ── Initialize database teardown ────────────────────────
    init_db(app)

    # ── Register blueprints ─────────────────────────────────
    from app.routes.auth          import auth_bp
    from app.routes.client        import client_bp
    from app.routes.freelancer    import freelancer_bp
    from app.routes.projects      import projects_bp
    from app.routes.proposals     import proposals_bp
    from app.routes.chat          import chat_bp
    from app.routes.payment       import payment_bp
    from app.routes.reviews       import reviews_bp
    from app.routes.notifications import notifications_bp
    from app.routes.work          import work_bp
    from app.routes.main          import main_bp
    from app.routes.upload        import upload_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,          url_prefix='/auth')
    app.register_blueprint(client_bp,        url_prefix='/client')
    app.register_blueprint(freelancer_bp,    url_prefix='/freelancer')
    app.register_blueprint(projects_bp,      url_prefix='/projects')
    app.register_blueprint(proposals_bp,     url_prefix='/proposals')
    app.register_blueprint(chat_bp,          url_prefix='/chat')
    app.register_blueprint(payment_bp,       url_prefix='/payment')
    app.register_blueprint(reviews_bp,       url_prefix='/reviews')
    app.register_blueprint(notifications_bp, url_prefix='/notifications')
    app.register_blueprint(work_bp,          url_prefix='/work')
    app.register_blueprint(upload_bp,        url_prefix='/upload')

    # ── Serve uploads from external folder ──────────────────
    @app.route('/static/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


    # ── Custom error handlers ───────────────────────────────
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(413)
    def request_too_large(e):
        return render_template('errors/413.html'), 413

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    # ── Logging ─────────────────────────────────────────────
    if not app.debug:
        os.makedirs('logs', exist_ok=True)
        file_handler = RotatingFileHandler(
            'logs/app.log', maxBytes=1_048_576, backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(name)s: %(message)s'
        ))
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

    # ── Context Processor for User Avatar ──────────────────
    @app.context_processor
    def inject_user_avatar():
        def get_user_avatar(user_id, role):
            if not user_id or not role:
                return None
            try:
                from app.models.user import UserModel
                if role == 'client':
                    profile = UserModel.get_client_profile(user_id)
                else:
                    profile = UserModel.get_freelancer_profile(user_id)
                return profile.get('avatar') if profile else None
            except Exception:
                return None
        return dict(get_user_avatar=get_user_avatar)

    return app
