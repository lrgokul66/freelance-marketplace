"""
Main / Home Blueprint — landing page, freelancer search.
"""
from flask import Blueprint, render_template, request
from app.models.project import ProjectModel
from app.models.user import UserModel

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    latest_projects, _ = ProjectModel.search_projects(sort='latest', per_page=6)
    popular_projects, _ = ProjectModel.search_projects(sort='popular', per_page=6)
    categories = ProjectModel.get_categories()
    all_skills = UserModel.get_all_skills()
    return render_template('main/home.html',
                           latest_projects=latest_projects,
                           popular_projects=popular_projects,
                           categories=categories,
                           all_skills=all_skills)


@main_bp.route('/search/projects')
def search_projects():
    keyword     = request.args.get('q', '')
    category    = request.args.get('category', '')
    skill_id    = request.args.get('skill_id', type=int)
    budget_min  = request.args.get('budget_min', type=float)
    budget_max  = request.args.get('budget_max', type=float)
    exp_level   = request.args.get('experience_level', '')
    duration    = request.args.get('duration', '')
    sort        = request.args.get('sort', 'latest')
    page        = request.args.get('page', 1, type=int)

    projects, total = ProjectModel.search_projects(
        keyword=keyword, category=category, skill_id=skill_id,
        budget_min=budget_min, budget_max=budget_max,
        experience_level=exp_level, duration=duration,
        sort=sort, page=page
    )
    categories = ProjectModel.get_categories()
    all_skills = UserModel.get_all_skills()
    total_pages = (total + 11) // 12

    return render_template('main/search_projects.html',
                           projects=projects, total=total,
                           page=page, total_pages=total_pages,
                           categories=categories, all_skills=all_skills,
                           filters=request.args)


@main_bp.route('/search/freelancers')
def search_freelancers():
    keyword      = request.args.get('q', '')
    skill_id     = request.args.get('skill_id', type=int)
    availability = request.args.get('availability', '')
    page         = request.args.get('page', 1, type=int)

    freelancers, total = UserModel.search_freelancers(
        keyword=keyword, skill_id=skill_id,
        availability=availability, page=page
    )
    all_skills   = UserModel.get_all_skills()
    total_pages  = (total + 11) // 12

    return render_template('main/search_freelancers.html',
                           freelancers=freelancers, total=total,
                           page=page, total_pages=total_pages,
                           all_skills=all_skills,
                           filters=request.args)


@main_bp.route('/freelancer/<int:user_id>/profile')
def public_freelancer_profile(user_id):
    profile = UserModel.get_freelancer_profile(user_id)
    if not profile:
        from flask import abort
        abort(404)
    fp_id = profile['id']
    skills         = UserModel.get_freelancer_skills(fp_id)
    portfolio      = UserModel.get_portfolio(fp_id)
    education      = UserModel.get_education(fp_id)
    experience     = UserModel.get_experience(fp_id)
    certifications = UserModel.get_certifications(fp_id)
    rating_info    = UserModel.get_avg_rating(user_id)
    from app.models.review import ReviewModel
    reviews, _     = ReviewModel.get_for_user(user_id, per_page=5)
    return render_template('main/public_freelancer_profile.html',
                           profile=profile, freelancer=profile, fp=profile,
                           skills=skills, portfolio=portfolio,
                           education=education, experience=experience,
                           certifications=certifications,
                           avg_rating=rating_info['avg_rating'],
                           review_count=rating_info['total'],
                           reviews=reviews)
