"""
Work Submission Blueprint — freelancer uploads deliverables,
client approves / rejects / requests revision.
"""
import os
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, abort, send_from_directory,
                   current_app)
from app.routes.auth import login_required
from app.models.work import WorkModel
from app.models.project import ProjectModel
from app.models.notification import NotificationModel
from app.services.file_service import save_upload

work_bp = Blueprint('work', __name__)


@work_bp.route('/submit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def submit(project_id):
    if session.get('role') != 'freelancer':
        abort(403)

    project = ProjectModel.get_by_id(project_id)
    if not project or project.get('hired_freelancer_id') != session['user_id']:
        abort(403)
    if project['status'] != 'in_progress':
        flash('Project is not in progress.', 'warning')
        return redirect(url_for('freelancer.dashboard'))

    if request.method == 'POST':
        chunked_files = request.form.getlist('chunked_attachments')
        notes = request.form.get('notes', '').strip()
        try:
            if chunked_files and chunked_files[0]:
                filename = chunked_files[0]
                src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                dest_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'work_submissions')
                os.makedirs(dest_dir, exist_ok=True)
                dest_path = os.path.join(dest_dir, filename)
                if os.path.exists(src_path):
                    import shutil
                    shutil.move(src_path, dest_path)
                orig_name = filename.split('_', 1)[-1] if '_' in filename else filename
                WorkModel.submit(project_id, session['user_id'], filename, orig_name, notes)
            else:
                f = request.files.get('work_file')
                saved, orig = save_upload(f, 'work_submissions',
                                          current_app.config['ALLOWED_WORK_EXTENSIONS'])
                WorkModel.submit(project_id, session['user_id'], saved, orig, notes)
            
            # Notify client
            NotificationModel.create(
                project['client_id'], 'work_submitted',
                'Work Submitted',
                f"{session['first_name']} submitted work for: {project['title']}",
                link=url_for('client.view_project', project_id=project_id)
            )
            flash('Work submitted for review!', 'success')
            return redirect(url_for('freelancer.dashboard'))
        except ValueError as e:
            flash(str(e), 'danger')

    return render_template('work/submit.html', project=project)


@work_bp.route('/review/<int:submission_id>', methods=['POST'])
@login_required
def review_submission(submission_id):
    if session.get('role') != 'client':
        abort(403)

    submission = WorkModel.get_by_id(submission_id)
    if not submission:
        abort(404)

    project = ProjectModel.get_by_id(submission['project_id'])
    if not project or project['client_id'] != session['user_id']:
        abort(403)

    status   = request.form.get('decision')   # approved / rejected / revision_requested
    feedback = request.form.get('feedback', '').strip()

    if status not in ('approved', 'rejected', 'revision_requested'):
        flash('Invalid decision.', 'danger')
        return redirect(url_for('client.view_project', project_id=project['id']))

    WorkModel.review(submission_id, status, feedback)

    notif_messages = {
        'approved':           ('Work Approved!', f"Your work for '{project['title']}' was approved."),
        'rejected':           ('Work Rejected', f"Your work for '{project['title']}' was rejected. Feedback: {feedback}"),
        'revision_requested': ('Revision Requested', f"Client requested revisions for '{project['title']}': {feedback}"),
    }
    title, msg = notif_messages[status]
    NotificationModel.create(
        submission['freelancer_id'], 'work_reviewed', title, msg,
        link=url_for('projects.detail', project_id=project['id'])
    )

    flash(f'Work {status.replace("_", " ")}.', 'success')
    return redirect(url_for('client.view_project', project_id=project['id']))


@work_bp.route('/download/<path:filename>')
@login_required
def download(filename):
    """Serve a work submission file for download."""
    upload_root = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    submissions_dir = os.path.join(upload_root, 'work_submissions')
    return send_from_directory(submissions_dir, filename, as_attachment=True)
