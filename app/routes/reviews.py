"""
Reviews Blueprint — submit ratings after project completion.
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, abort)
from app.routes.auth import login_required
from app.models.review import ReviewModel
from app.models.project import ProjectModel
from app.models.notification import NotificationModel

reviews_bp = Blueprint('reviews', __name__)


@reviews_bp.route('/submit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def submit(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['status'] != 'completed':
        flash('Reviews can only be left for completed projects.', 'warning')
        return redirect(url_for('main.home'))

    uid  = session['user_id']
    role = session['role']

    # Determine reviewee
    if role == 'client' and project['client_id'] == uid:
        reviewee_id = project.get('hired_freelancer_id')
    elif role == 'freelancer' and project.get('hired_freelancer_id') == uid:
        reviewee_id = project['client_id']
    else:
        abort(403)

    if ReviewModel.already_reviewed(project_id, uid):
        flash('You have already reviewed this project.', 'info')
        return redirect(url_for('main.home'))

    if request.method == 'POST':
        rating  = int(request.form.get('rating', 5))
        comment = request.form.get('comment', '').strip()
        if not 1 <= rating <= 5:
            flash('Rating must be between 1 and 5.', 'danger')
        else:
            ReviewModel.create(project_id, uid, reviewee_id, rating, comment)
            NotificationModel.create(
                reviewee_id, 'rating_received',
                'New Review Received',
                f"You received a {rating}-star review!",
                link=url_for('main.home')
            )
            flash('Review submitted. Thank you!', 'success')
            return redirect(url_for('main.home'))

    return render_template('reviews/submit.html', project=project)
