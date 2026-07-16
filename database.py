"""
Database connection helper for the Freelance Marketplace app.
Uses PyMySQL with a per-request connection pattern via Flask's g object.
"""
import pymysql
import pymysql.cursors
from flask import g, current_app
import logging

logger = logging.getLogger(__name__)


def get_db():
    """
    Open a new database connection if there is none in the current
    application context.
    """
    if 'db' not in g:
        try:
            # Enable SSL automatically if explicitly configured or using a remote database host
            ssl_config = None
            db_host = current_app.config['MYSQL_HOST']
            if current_app.config.get('MYSQL_SSL') or (db_host not in ('localhost', '127.0.0.1')):
                ssl_config = {'ssl': {}}

            g.db = pymysql.connect(
                host=db_host,
                port=current_app.config['MYSQL_PORT'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=False,
                ssl=ssl_config,
                init_command=(
                    "SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,"
                    "NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION'"
                ),
            )
        except pymysql.MySQLError as e:
            logger.error(f"Database connection failed: {e}")
            raise
    return g.db


def close_db(e=None):
    """Close the database connection at the end of the request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def execute_query(query, params=None, fetch='all', commit=False):
    """
    Execute a parameterized SQL query safely.

    Args:
        query   : SQL string with %s placeholders
        params  : tuple / list of parameters
        fetch   : 'all' | 'one' | 'none'
        commit  : whether to commit after execution

    Returns:
        Result rows (dict or list of dicts) or lastrowid for INSERT.
    """
    db = get_db()
    try:
        with db.cursor() as cursor:
            cursor.execute(query, params or ())
            if commit:
                db.commit()
                return cursor.lastrowid
            if fetch == 'one':
                return cursor.fetchone()
            if fetch == 'all':
                return cursor.fetchall()
            return None
    except pymysql.MySQLError as e:
        db.rollback()
        logger.error(f"Query error: {e}\nQuery: {query}\nParams: {params}")
        raise


def init_db(app):
    """Register the teardown function with the app."""
    app.teardown_appcontext(close_db)
