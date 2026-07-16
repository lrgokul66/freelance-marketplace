"""
Freelancer Blueprint — dashboard, full profile (skills, portfolio, education,
experience, certifications), browse projects, saved projects.
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app, abort)
from app.routes.auth import login_required, role_required
from app.models.user import UserModel
from app.models.project import ProjectModel
from app.models.proposal import ProposalModel
from app.models.payment import PaymentModel
from app.models.notification import NotificationModel
from app.models.message import MessageModel
from app.services.file_service import save_upload

freelancer_bp = Blueprint('freelancer', __name__)


# ── Dashboard ─────────────────────────────────────────────────
@freelancer_bp.route('/dashboard')
@role_required('freelancer')
def dashboard():
    uid = session['user_id']
    proposals, total_proposals = ProposalModel.get_by_freelancer(uid)
    available_projects, _ = ProjectModel.search_projects(sort='latest', per_page=6)
    total_earnings = PaymentModel.get_total_earnings(uid)
    rating_info    = UserModel.get_avg_rating(uid)
    notif_count    = NotificationModel.get_unread_count(uid)
    msg_count      = MessageModel.get_unread_count(uid)

    accepted   = [p for p in proposals if p['status'] == 'accepted']
    completed  = [p for p in proposals if p['project_status'] == 'completed']
    pending    = [p for p in proposals if p['status'] == 'pending']

    return render_template('freelancer/dashboard.html',
                           proposals=proposals[:5],
                           total_proposals=total_proposals,
                           available_projects=available_projects,
                           accepted_count=len(accepted),
                           completed_count=len(completed),
                           pending_count=len(pending),
                           total_earnings=total_earnings,
                           rating_info=rating_info,
                           notif_count=notif_count,
                           msg_count=msg_count)


# ── Profile ───────────────────────────────────────────────────
@freelancer_bp.route('/profile')
@role_required('freelancer')
def profile():
    uid = session['user_id']
    profile        = UserModel.get_freelancer_profile(uid)
    fp_id          = profile['id']
    skills         = UserModel.get_freelancer_skills(fp_id)
    portfolio      = UserModel.get_portfolio(fp_id)
    education      = UserModel.get_education(fp_id)
    experience     = UserModel.get_experience(fp_id)
    certifications = UserModel.get_certifications(fp_id)
    rating_info    = UserModel.get_avg_rating(uid)
    from app.models.review import ReviewModel
    reviews, _     = ReviewModel.get_for_user(uid)
    return render_template('freelancer/profile.html',
                           profile=profile, skills=skills,
                           portfolio=portfolio, education=education,
                           experience=experience, certifications=certifications,
                           rating_info=rating_info, reviews=reviews)


@freelancer_bp.route('/profile/edit', methods=['GET', 'POST'])
@role_required('freelancer')
def edit_profile():
    uid     = session['user_id']
    profile = UserModel.get_freelancer_profile(uid)
    fp_id   = profile['id']
    all_skills     = UserModel.get_all_skills()
    current_skills = UserModel.get_freelancer_skills(fp_id)
    current_skill_ids = [s['id'] for s in current_skills]

    if request.method == 'POST':
        action = request.form.get('action', 'update_profile')

        if action == 'update_profile':
            data = {
                'first_name':   request.form.get('first_name', '').strip(),
                'last_name':    request.form.get('last_name', '').strip(),
                'headline':     request.form.get('headline', '').strip(),
                'bio':          request.form.get('bio', '').strip(),
                'hourly_rate':  request.form.get('hourly_rate', 0) or 0,
                'availability': request.form.get('availability', 'full_time'),
                'languages':    request.form.get('languages', '').strip(),
            }
            UserModel.update_freelancer_profile(uid, data)
            session['first_name'] = data['first_name']
            session['last_name']  = data['last_name']
            flash('Profile updated.', 'success')

        elif action == 'update_skills':
            skill_ids = [int(s) for s in request.form.getlist('skills') if s.isdigit()]
            new_skill = request.form.get('new_skill', '').strip()
            if new_skill:
                sid = UserModel.get_or_create_skill(new_skill)
                skill_ids.append(sid)
            UserModel.set_freelancer_skills(fp_id, skill_ids)
            flash('Skills updated.', 'success')

        elif action == 'upload_avatar':
            f = request.files.get('avatar')
            try:
                fname, _ = save_upload(f, 'avatars',
                                       current_app.config['ALLOWED_IMAGE_EXTENSIONS'])
                UserModel.update_freelancer_avatar(uid, fname)
                flash('Profile picture updated.', 'success')
            except ValueError as e:
                flash(str(e), 'danger')

        elif action == 'upload_resume':
            f = request.files.get('resume')
            try:
                fname, _ = save_upload(f, 'resumes',
                                       current_app.config['ALLOWED_RESUME_EXTENSIONS'])
                UserModel.update_freelancer_resume(uid, fname)
                flash('Resume uploaded.', 'success')
            except ValueError as e:
                flash(str(e), 'danger')

        elif action == 'add_portfolio':
            title       = request.form.get('portfolio_title', '').strip()
            description = request.form.get('portfolio_desc', '').strip()
            link        = request.form.get('portfolio_link', '').strip()
            image_name  = None
            f = request.files.get('portfolio_image')
            if f and f.filename:
                try:
                    image_name, _ = save_upload(f, 'portfolios',
                                                current_app.config['ALLOWED_IMAGE_EXTENSIONS'])
                except ValueError:
                    pass
            UserModel.add_portfolio(fp_id, title, description, image_name, link)
            flash('Portfolio item added.', 'success')

        elif action == 'delete_portfolio':
            pid = request.form.get('portfolio_id', type=int)
            UserModel.delete_portfolio(pid, fp_id)
            flash('Portfolio item removed.', 'info')

        elif action == 'add_education':
            UserModel.add_education(
                fp_id,
                request.form.get('degree', '').strip(),
                request.form.get('institution', '').strip(),
                request.form.get('edu_year', '') or None,
                request.form.get('edu_desc', '').strip()
            )
            flash('Education added.', 'success')

        elif action == 'delete_education':
            eid = request.form.get('edu_id', type=int)
            UserModel.delete_education(eid, fp_id)
            flash('Education removed.', 'info')

        elif action == 'add_experience':
            UserModel.add_experience(
                fp_id,
                request.form.get('exp_title', '').strip(),
                request.form.get('exp_company', '').strip(),
                request.form.get('exp_years', '').strip(),
                request.form.get('exp_desc', '').strip()
            )
            flash('Experience added.', 'success')

        elif action == 'delete_experience':
            eid = request.form.get('exp_id', type=int)
            UserModel.delete_experience(eid, fp_id)
            flash('Experience removed.', 'info')

        elif action == 'add_certification':
            UserModel.add_certification(
                fp_id,
                request.form.get('cert_name', '').strip(),
                request.form.get('cert_issuer', '').strip(),
                request.form.get('cert_year', '') or None
            )
            flash('Certification added.', 'success')

        elif action == 'delete_certification':
            cid = request.form.get('cert_id', type=int)
            UserModel.delete_certification(cid, fp_id)
            flash('Certification removed.', 'info')

        return redirect(url_for('freelancer.edit_profile'))

    portfolio      = UserModel.get_portfolio(fp_id)
    education      = UserModel.get_education(fp_id)
    experience     = UserModel.get_experience(fp_id)
    certifications = UserModel.get_certifications(fp_id)

    return render_template('freelancer/edit_profile.html',
                           profile=profile, all_skills=all_skills,
                           current_skill_ids=current_skill_ids,
                           portfolio=portfolio, education=education,
                           experience=experience, certifications=certifications)


# ── Browse Projects ───────────────────────────────────────────
@freelancer_bp.route('/browse')
@role_required('freelancer')
def browse_projects():
    keyword    = request.args.get('q', '')
    category   = request.args.get('category', '')
    skill_id   = request.args.get('skill_id', type=int)
    budget_min = request.args.get('budget_min', type=float)
    budget_max = request.args.get('budget_max', type=float)
    exp_level  = request.args.get('experience_level', '')
    duration   = request.args.get('duration', '')
    sort       = request.args.get('sort', 'latest')
    page       = request.args.get('page', 1, type=int)

    projects, total = ProjectModel.search_projects(
        keyword=keyword, category=category, skill_id=skill_id,
        budget_min=budget_min, budget_max=budget_max,
        experience_level=exp_level, duration=duration,
        sort=sort, page=page
    )
    categories  = ProjectModel.get_categories()
    all_skills  = UserModel.get_all_skills()
    total_pages = (total + 11) // 12

    return render_template('freelancer/browse.html',
                           projects=projects, total=total,
                           page=page, total_pages=total_pages,
                           categories=categories, all_skills=all_skills,
                           filters=request.args)


# ── Saved Projects ────────────────────────────────────────────
@freelancer_bp.route('/saved-projects')
@role_required('freelancer')
def saved_projects():
    projects = ProjectModel.get_saved_projects(session['user_id'])
    return render_template('freelancer/saved_projects.html', projects=projects)


@freelancer_bp.route('/save-project/<int:project_id>', methods=['POST'])
@role_required('freelancer')
def toggle_save_project(project_id):
    uid = session['user_id']
    if ProjectModel.is_saved(uid, project_id):
        ProjectModel.unsave_project(uid, project_id)
        flash('Project removed from saved.', 'info')
    else:
        ProjectModel.save_project(uid, project_id)
        flash('Project saved!', 'success')
    return redirect(request.referrer or url_for('freelancer.browse_projects'))


# ── My Proposals ──────────────────────────────────────────────
@freelancer_bp.route('/proposals')
@role_required('freelancer')
def my_proposals():
    page = request.args.get('page', 1, type=int)
    proposals, total = ProposalModel.get_by_freelancer(session['user_id'], page=page)
    total_pages = (total + 9) // 10
    return render_template('freelancer/proposals.html',
                           proposals=proposals, total=total,
                           page=page, total_pages=total_pages)
