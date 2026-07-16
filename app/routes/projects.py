"""
Projects Blueprint — public project listing and individual project detail.
"""
from flask import Blueprint, render_template, request, abort
from app.models.project import ProjectModel
from app.models.user import UserModel
from app.models.proposal import ProposalModel
from app.models.review import ReviewModel

projects_bp = Blueprint('projects', __name__)


@projects_bp.route('/')
def list_projects():
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

    return render_template('projects/list.html',
                           projects=projects, total=total,
                           page=page, total_pages=total_pages,
                           categories=categories, all_skills=all_skills,
                           filters=request.args)


@projects_bp.route('/<int:project_id>')
def detail(project_id):
    project = ProjectModel.get_by_id(project_id)
    if not project:
        abort(404)
    ProjectModel.increment_views(project_id)
    skills   = ProjectModel.get_project_skills(project_id)
    files    = ProjectModel.get_files(project_id)
    reviews  = ReviewModel.get_for_project(project_id)
    return render_template('projects/detail.html',
                           project=project, skills=skills,
                           files=files, reviews=reviews)
