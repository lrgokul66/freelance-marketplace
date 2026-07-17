"""
Proposals Blueprint — freelancer submits, edits, withdraws, views proposals.
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app, abort, send_from_directory)
from app.routes.auth import role_required, login_required
from app.models.proposal import ProposalModel
from app.models.project import ProjectModel
from app.models.notification import NotificationModel
from app.services.file_service import save_upload

proposals_bp = Blueprint('proposals', __name__)


@proposals_bp.route('/project/<int:project_id>/submit', methods=['GET', 'POST'])
@role_required('freelancer')
def submit(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['status'] not in ('open', 'hiring'):
        flash('This project is not accepting proposals.', 'warning')
        return redirect(url_for('freelancer.browse_projects'))

    existing = ProposalModel.already_proposed(project_id, session['user_id'])
    if existing:
        flash('You have already submitted a proposal for this project.', 'info')
        return redirect(url_for('proposals.view', proposal_id=existing['id']))

    if request.method == 'POST':
        data = {
            'cover_letter':   request.form.get('cover_letter', '').strip(),
            'bid_amount':     float(request.form.get('bid_amount', 0) or 0),
            'delivery_days':  int(request.form.get('delivery_days', 7) or 7),
            'portfolio_links': request.form.get('portfolio_links', '').strip(),
        }
        if not data['cover_letter']:
            flash('Cover letter is required.', 'danger')
            return render_template('proposals/submit.html', project=project)

        try:
            proposal_id = ProposalModel.create(project_id, session['user_id'], data)

            # Handle chunked uploads
            chunked_files = request.form.getlist('chunked_attachments')
            for filename in chunked_files:
                if filename:
                    import os
                    import shutil
                    src_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    dest_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], 'proposal_files')
                    os.makedirs(dest_dir, exist_ok=True)
                    dest_path = os.path.join(dest_dir, filename)
                    if os.path.exists(src_path):
                        shutil.move(src_path, dest_path)
                    orig_name = filename.split('_', 1)[-1] if '_' in filename else filename
                    ProposalModel.add_file(proposal_id, filename, orig_name)

            # Handle standard attachments (fallback)
            files = request.files.getlist('attachments')
            for f in files:
                if f and f.filename:
                    try:
                        fname, orig = save_upload(
                            f, 'proposal_files',
                            current_app.config['ALLOWED_DOC_EXTENSIONS'] |
                            current_app.config['ALLOWED_IMAGE_EXTENSIONS']
                        )
                        ProposalModel.add_file(proposal_id, fname, orig)
                    except ValueError:
                        pass

            # Notify client
            NotificationModel.create(
                project['client_id'], 'new_proposal',
                'New Proposal Received',
                f"{session['first_name']} submitted a proposal for: {project['title']}",
                link=url_for('client.view_project', project_id=project_id)
            )

            flash('Proposal submitted!', 'success')
            return redirect(url_for('proposals.view', proposal_id=proposal_id))
        except Exception as ex:
            current_app.logger.error(f"Proposal submit error: {ex}")
            flash('Error submitting proposal.', 'danger')

    return render_template('proposals/submit.html', project=project)


@proposals_bp.route('/<int:proposal_id>')
@role_required('freelancer')
def view(proposal_id):
    proposal = ProposalModel.get_by_id(proposal_id)
    if not proposal or proposal['freelancer_id'] != session['user_id']:
        abort(403)
    files = ProposalModel.get_files(proposal_id)
    return render_template('proposals/view.html', proposal=proposal, files=files)


@proposals_bp.route('/<int:proposal_id>/edit', methods=['GET', 'POST'])
@role_required('freelancer')
def edit(proposal_id):
    proposal = ProposalModel.get_by_id(proposal_id)
    if not proposal or proposal['freelancer_id'] != session['user_id']:
        abort(403)
    if proposal['status'] not in ('pending', 'shortlisted'):
        flash('This proposal cannot be edited.', 'warning')
        return redirect(url_for('proposals.view', proposal_id=proposal_id))

    if request.method == 'POST':
        data = {
            'cover_letter':    request.form.get('cover_letter', '').strip(),
            'bid_amount':      float(request.form.get('bid_amount', 0) or 0),
            'delivery_days':   int(request.form.get('delivery_days', 7) or 7),
            'portfolio_links': request.form.get('portfolio_links', '').strip(),
        }
        ProposalModel.update(proposal_id, session['user_id'], data)
        flash('Proposal updated.', 'success')
        return redirect(url_for('proposals.view', proposal_id=proposal_id))

    project = ProjectModel.get_by_id(proposal['project_id'])
    files = ProposalModel.get_files(proposal_id)
    return render_template('proposals/edit.html', proposal=proposal, project=project, files=files)


@proposals_bp.route('/<int:proposal_id>/withdraw', methods=['POST'])
@role_required('freelancer')
def withdraw(proposal_id):
    proposal = ProposalModel.get_by_id(proposal_id)
    if not proposal or proposal['freelancer_id'] != session['user_id']:
        abort(403)
    ProposalModel.withdraw(proposal_id, session['user_id'])
    flash('Proposal withdrawn.', 'info')
    return redirect(url_for('freelancer.my_proposals'))


@proposals_bp.route('/<int:proposal_id>/delete', methods=['POST'])
@role_required('freelancer')
def delete(proposal_id):
    proposal = ProposalModel.get_by_id(proposal_id)
    if not proposal or proposal['freelancer_id'] != session['user_id']:
        abort(403)
    ProposalModel.delete(proposal_id, session['user_id'])
    flash('Proposal deleted.', 'info')
    return redirect(url_for('freelancer.my_proposals'))


@proposals_bp.route('/download/<path:filename>')
@login_required
def download_attachment(filename):
    """Serve a proposal attachment file for download."""
    import os
    upload_root = current_app.config.get('UPLOAD_FOLDER', 'uploads')
    proposal_files_dir = os.path.join(upload_root, 'proposal_files')
    return send_from_directory(proposal_files_dir, filename, as_attachment=True)

