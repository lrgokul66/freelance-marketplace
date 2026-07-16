"""
Chat Blueprint — private messaging between client and freelancer per project.
Supports text messages, image/file uploads, read status, and AJAX polling.
"""
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, abort, jsonify, current_app)
from app.routes.auth import login_required
from app.models.message import MessageModel
from app.models.project import ProjectModel
from app.models.user import UserModel
from app.services.file_service import save_upload

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
@login_required
def inbox():
    conversations = MessageModel.get_conversations_for_user(session['user_id'])
    return render_template('chat/inbox.html', conversations=conversations)


@chat_bp.route('/project/<int:project_id>/with/<int:other_user_id>')
@login_required
def conversation(project_id, other_user_id):
    project = ProjectModel.get_by_id(project_id)
    if not project:
        abort(404)

    uid = session['user_id']

    # Authorization — only client or hired freelancer may chat
    is_client     = (project['client_id'] == uid)
    is_freelancer = (project.get('hired_freelancer_id') == uid and uid == other_user_id
                     or project.get('hired_freelancer_id') == other_user_id and is_client)

    if not (is_client or uid == project.get('hired_freelancer_id')):
        # Allow if either party in the conversation
        if uid != other_user_id and uid != project['client_id'] and \
           uid != project.get('hired_freelancer_id'):
            abort(403)

    other_user = UserModel.get_by_id(other_user_id)
    if not other_user:
        abort(404)

    messages = MessageModel.get_conversation(project_id, uid, other_user_id)
    MessageModel.mark_read(project_id, uid)

    return render_template('chat/conversation.html',
                           project=project,
                           other_user=other_user,
                           messages=messages)


@chat_bp.route('/send', methods=['POST'])
@login_required
def send_message():
    project_id    = request.form.get('project_id', type=int)
    receiver_id   = request.form.get('receiver_id', type=int)
    content       = request.form.get('content', '').strip()
    file_path     = None
    file_name     = None

    if not project_id or not receiver_id:
        flash('Invalid message.', 'danger')
        return redirect(url_for('chat.inbox'))

    # Handle file attachment
    f = request.files.get('file')
    if f and f.filename:
        try:
            saved, orig = save_upload(
                f, 'chat_files',
                current_app.config['ALLOWED_DOC_EXTENSIONS'] |
                current_app.config['ALLOWED_IMAGE_EXTENSIONS']
            )
            file_path = saved
            file_name = orig
        except ValueError as e:
            flash(str(e), 'danger')

    if not content and not file_path:
        flash('Message cannot be empty.', 'warning')
        return redirect(url_for('chat.conversation',
                                project_id=project_id, other_user_id=receiver_id))

    MessageModel.send(session['user_id'], receiver_id, project_id,
                      content or None, file_path, file_name)

    # Notify receiver via notification model
    from app.models.notification import NotificationModel
    from app.models.project import ProjectModel as PM
    project = PM.get_by_id(project_id)
    NotificationModel.create(
        receiver_id, 'new_message',
        'New Message',
        f"{session['first_name']} sent you a message on: {project['title'] if project else ''}",
        link=url_for('chat.conversation', project_id=project_id,
                     other_user_id=session['user_id'])
    )

    return redirect(url_for('chat.conversation',
                            project_id=project_id, other_user_id=receiver_id))


@chat_bp.route('/poll/<int:project_id>/<int:other_user_id>')
@login_required
def poll_messages(project_id, other_user_id):
    """AJAX endpoint to fetch new messages since last_id."""
    last_id = request.args.get('last_id', 0, type=int)
    uid     = session['user_id']
    messages = MessageModel.get_new_messages_since(project_id, uid, other_user_id, last_id)
    MessageModel.mark_read(project_id, uid)

    result = []
    for m in messages:
        result.append({
            'id':           m['id'],
            'sender_id':    m['sender_id'],
            'content':      m['content'],
            'file_path':    m['file_path'],
            'file_name':    m['file_name'],
            'is_read':      m['is_read'],
            'first_name':   m['first_name'],
            'sender_avatar': m['sender_avatar'],
            'created_at':   m['created_at'].strftime('%H:%M') if m.get('created_at') else '',
        })
    return jsonify(messages=result)


@chat_bp.route('/unread-count')
@login_required
def unread_count():
    count = MessageModel.get_unread_count(session['user_id'])
    return jsonify(count=count)
