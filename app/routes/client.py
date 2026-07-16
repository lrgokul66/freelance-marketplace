"""
Client Blueprint — dashboard, profile management, project CRUD,
proposal management (view/accept/reject/shortlist/hire).
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app, abort, jsonify)
from app.routes.auth import login_required, role_required
from app.models.user import UserModel
from app.models.project import ProjectModel
from app.models.proposal import ProposalModel
from app.models.notification import NotificationModel
from app.models.message import MessageModel
from app.models.payment import PaymentModel
from app.services.file_service import save_upload

client_bp = Blueprint('client', __name__)

# ── Dashboard ─────────────────────────────────────────────────
@client_bp.route('/dashboard')
@role_required('client')
def dashboard():
    uid = session['user_id']
    projects = ProjectModel.get_by_client(uid)
    status_counts = {s: 0 for s in ['open','hiring','in_progress','completed','closed']}
    for p in projects:
        s = p.get('status','open')
        status_counts[s] = status_counts.get(s, 0) + 1

    pending_proposals = sum(p.get('proposal_count', 0) for p in projects if p['status'] in ('open','hiring'))
    payments = PaymentModel.get_history(uid, 'client')
    recent_payments = payments[:5]
    notif_count = NotificationModel.get_unread_count(uid)
    msg_count   = MessageModel.get_unread_count(uid)

    return render_template('client/dashboard.html',
                           projects=projects[:5],
                           status_counts=status_counts,
                           pending_proposals=pending_proposals,
                           recent_payments=recent_payments,
                           notif_count=notif_count,
                           msg_count=msg_count)


# ── Profile ───────────────────────────────────────────────────
@client_bp.route('/profile')
@role_required('client')
def profile():
    profile = UserModel.get_client_profile(session['user_id'])
    from app.models.review import ReviewModel
    reviews, _ = ReviewModel.get_for_user(session['user_id'])
    rating_info = UserModel.get_avg_rating(session['user_id'])
    projects = ProjectModel.get_by_client(session['user_id'])
    status_counts = {s: 0 for s in ['open', 'hiring', 'in_progress', 'completed', 'closed']}
    for p in projects:
        s = p.get('status', 'open')
        status_counts[s] = status_counts.get(s, 0) + 1
    completed = [p for p in projects if p['status'] == 'completed']
    return render_template('client/profile.html',
                           profile=profile, reviews=reviews,
                           rating_info=rating_info,
                           completed_count=len(completed),
                           status_counts=status_counts)


@client_bp.route('/profile/edit', methods=['GET', 'POST'])
@role_required('client')
def edit_profile():
    uid = session['user_id']
    profile = UserModel.get_client_profile(uid)

    if request.method == 'POST':
        action = request.form.get('action', 'update_profile')

        if action == 'update_profile':
            data = {
                'first_name':  request.form.get('first_name', '').strip(),
                'last_name':   request.form.get('last_name', '').strip(),
                'company':     request.form.get('company', '').strip(),
                'website':     request.form.get('website', '').strip(),
                'location':    request.form.get('location', '').strip(),
                'phone':       request.form.get('phone', '').strip(),
                'description': request.form.get('description', '').strip(),
            }
            UserModel.update_client_profile(uid, data)
            session['first_name'] = data['first_name']
            session['last_name']  = data['last_name']
            flash('Profile updated.', 'success')

        elif action == 'upload_avatar':
            f = request.files.get('avatar')
            try:
                fname, _ = save_upload(f, 'avatars',
                                       current_app.config['ALLOWED_IMAGE_EXTENSIONS'])
                UserModel.update_client_avatar(uid, fname)
                flash('Profile picture updated.', 'success')
            except ValueError as e:
                flash(str(e), 'danger')

        return redirect(url_for('client.edit_profile'))

    return render_template('client/edit_profile.html', profile=profile)


# ── Projects ──────────────────────────────────────────────────
@client_bp.route('/projects')
@role_required('client')
def my_projects():
    projects = ProjectModel.get_by_client(session['user_id'])
    return render_template('client/projects.html', projects=projects)


@client_bp.route('/projects/create', methods=['GET', 'POST'])
@role_required('client')
def create_project():
    all_skills = UserModel.get_all_skills()

    if request.method == 'POST':
        data = {
            'title':            request.form.get('title', '').strip(),
            'category':         request.form.get('category', '').strip(),
            'description':      request.form.get('description', '').strip(),
            'budget_min':       float(request.form.get('budget_min', 0) or 0),
            'budget_max':       float(request.form.get('budget_max', 0) or 0),
            'experience_level': request.form.get('experience_level', 'intermediate'),
            'duration':         request.form.get('duration', '').strip(),
            'deadline':         request.form.get('deadline', '').strip() or None,
        }
        skill_ids = request.form.getlist('skills')
        new_skill = request.form.get('new_skill', '').strip()

        if not all([data['title'], data['category'], data['description']]):
            flash('Title, category and description are required.', 'danger')
            categories = ProjectModel.get_categories()
            return render_template('client/create_project.html',
                                   all_skills=all_skills, categories=categories, form=request.form)

        try:
            project_id = ProjectModel.create_project(session['user_id'], data)
            # Handle skills
            final_skill_ids = [int(s) for s in skill_ids if s.isdigit()]
            if new_skill:
                sid = UserModel.get_or_create_skill(new_skill)
                final_skill_ids.append(sid)
            ProjectModel.set_project_skills(project_id, final_skill_ids)

            # Handle file attachments
            files = request.files.getlist('attachments')
            for f in files:
                if f and f.filename:
                    try:
                        fname, orig = save_upload(
                            f, 'project_files',
                            current_app.config['ALLOWED_DOC_EXTENSIONS'] |
                            current_app.config['ALLOWED_IMAGE_EXTENSIONS']
                        )
                        ProjectModel.add_file(project_id, fname, orig)
                    except ValueError:
                        pass  # skip invalid files silently

            flash('Project posted successfully!', 'success')
            return redirect(url_for('client.view_project', project_id=project_id))
        except Exception as ex:
            current_app.logger.error(f"Create project error: {ex}")
            flash('Error creating project. Please try again.', 'danger')

    categories = ProjectModel.get_categories()
    return render_template('client/create_project.html',
                           all_skills=all_skills, categories=categories, form={})


@client_bp.route('/projects/<int:project_id>')
@role_required('client')
def view_project(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    skills   = ProjectModel.get_project_skills(project_id)
    files    = ProjectModel.get_files(project_id)
    proposals = ProposalModel.get_by_project(project_id)
    from app.models.work import WorkModel
    submissions = WorkModel.get_by_project(project_id)
    payment = PaymentModel.get_by_project(project_id)
    from app.models.review import ReviewModel
    already_reviewed = ReviewModel.already_reviewed(project_id, session['user_id'])
    return render_template('client/view_project.html',
                           project=project, skills=skills, files=files,
                           proposals=proposals, submissions=submissions,
                           payment=payment, already_reviewed=already_reviewed)


@client_bp.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@role_required('client')
def edit_project(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    if project['status'] not in ('open', 'hiring'):
        flash('Only open or hiring projects can be edited.', 'warning')
        return redirect(url_for('client.view_project', project_id=project_id))

    all_skills     = UserModel.get_all_skills()
    current_skills = ProjectModel.get_project_skills(project_id)
    current_skill_ids = [s['id'] for s in current_skills]

    if request.method == 'POST':
        data = {
            'title':            request.form.get('title', '').strip(),
            'category':         request.form.get('category', '').strip(),
            'description':      request.form.get('description', '').strip(),
            'budget_min':       float(request.form.get('budget_min', 0) or 0),
            'budget_max':       float(request.form.get('budget_max', 0) or 0),
            'experience_level': request.form.get('experience_level', 'intermediate'),
            'duration':         request.form.get('duration', '').strip(),
            'deadline':         request.form.get('deadline', '').strip() or None,
        }
        skill_ids = [int(s) for s in request.form.getlist('skills') if s.isdigit()]
        new_skill = request.form.get('new_skill', '').strip()
        if new_skill:
            sid = UserModel.get_or_create_skill(new_skill)
            skill_ids.append(sid)

        ProjectModel.update_project(project_id, data)
        ProjectModel.set_project_skills(project_id, skill_ids)
        flash('Project updated.', 'success')
        return redirect(url_for('client.view_project', project_id=project_id))

    categories = ProjectModel.get_categories()
    return render_template('client/edit_project.html',
                           project=project, all_skills=all_skills,
                           categories=categories,
                           current_skill_ids=current_skill_ids)


@client_bp.route('/projects/<int:project_id>/delete', methods=['POST'])
@role_required('client')
def delete_project(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    if project['status'] == 'in_progress':
        flash('Cannot delete an in-progress project.', 'danger')
        return redirect(url_for('client.view_project', project_id=project_id))
    ProjectModel.delete_project(project_id, session['user_id'])
    flash('Project deleted.', 'success')
    return redirect(url_for('client.my_projects'))


@client_bp.route('/projects/<int:project_id>/close', methods=['POST'])
@role_required('client')
def close_project(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    ProjectModel.update_status(project_id, 'closed')
    flash('Project closed.', 'info')
    return redirect(url_for('client.view_project', project_id=project_id))


@client_bp.route('/projects/<int:project_id>/reopen', methods=['POST'])
@role_required('client')
def reopen_project(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    if project['status'] == 'closed':
        ProjectModel.update_status(project_id, 'open')
        flash('Project reopened.', 'success')
    return redirect(url_for('client.view_project', project_id=project_id))


# ── Proposal Actions ──────────────────────────────────────────
@client_bp.route('/proposals/<int:proposal_id>/action', methods=['POST'])
@role_required('client')
def proposal_action(proposal_id):
    proposal = ProposalModel.get_by_id(proposal_id)
    if not proposal:
        abort(404)

    project = ProjectModel.get_by_id(proposal['project_id'])
    if not project or project['client_id'] != session['user_id']:
        abort(403)

    action = request.form.get('action')
    note   = request.form.get('client_note', '').strip()

    if action == 'shortlist':
        ProposalModel.update_status(proposal_id, 'shortlisted', note)
        flash('Proposal shortlisted.', 'info')

    elif action == 'accept':
        ProposalModel.update_status(proposal_id, 'accepted', note)
        # Reject all other proposals
        all_proposals = ProposalModel.get_by_project(proposal['project_id'])
        for p in all_proposals:
            if p['id'] != proposal_id and p['status'] not in ('withdrawn',):
                ProposalModel.update_status(p['id'], 'rejected')
        # Update project status to 'hiring'
        ProjectModel.update_status(proposal['project_id'], 'hiring')
        flash('Proposal accepted!', 'success')

    elif action == 'reject':
        ProposalModel.update_status(proposal_id, 'rejected', note)
        flash('Proposal rejected.', 'warning')

    elif action == 'hire':
        # Finalize hire — project goes In Progress, chat begins
        ProposalModel.update_status(proposal_id, 'accepted')
        ProjectModel.update_status(proposal['project_id'], 'in_progress',
                                   hired_freelancer_id=proposal['freelancer_id'])
        # Notify freelancer
        NotificationModel.create(
            proposal['freelancer_id'], 'hired',
            'You have been hired!',
            f"You've been hired for project: {project['title']}",
            link=url_for('chat.conversation',
                         project_id=proposal['project_id'],
                         other_user_id=session['user_id'])
        )
        flash('Freelancer hired! Chat is now open.', 'success')

    return redirect(url_for('client.view_project',
                            project_id=proposal['project_id']))


@client_bp.route('/proposals/compare/<int:project_id>')
@role_required('client')
def compare_proposals(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    proposals = ProposalModel.get_by_project(project_id)
    return render_template('client/compare_proposals.html',
                           project=project, proposals=proposals)
