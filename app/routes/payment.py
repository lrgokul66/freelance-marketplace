"""
Payment Blueprint — Razorpay integration, transaction history, invoice PDF.
"""
import hmac
import hashlib
import razorpay
from flask import (Blueprint, render_template, request, redirect,
                   url_for, session, flash, current_app, abort,
                   jsonify, make_response)
from app.routes.auth import login_required
from app.models.payment import PaymentModel
from app.models.project import ProjectModel
from app.models.notification import NotificationModel

payment_bp = Blueprint('payment', __name__)


def get_razorpay_client():
    return razorpay.Client(
        auth=(current_app.config['RAZORPAY_KEY_ID'],
              current_app.config['RAZORPAY_KEY_SECRET'])
    )


# ── Initiate Payment ──────────────────────────────────────────
@payment_bp.route('/initiate/<int:project_id>')
@login_required
def initiate(project_id):
    if session.get('role') != 'client':
        abort(403)

    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        abort(403)
    if project['status'] != 'in_progress':
        flash('Payment can only be made for in-progress projects.', 'warning')
        return redirect(url_for('client.view_project', project_id=project_id))

    # Check if already paid
    existing = PaymentModel.get_by_project(project_id)
    if existing and existing['status'] == 'completed':
        flash('Payment already completed.', 'info')
        return redirect(url_for('payment.history'))

    # Proposal accepted — use bid amount
    from app.models.proposal import ProposalModel
    proposals = ProposalModel.get_by_project(project_id)
    accepted  = next((p for p in proposals if p['status'] == 'accepted'), None)
    if not accepted:
        flash('No accepted proposal found.', 'danger')
        return redirect(url_for('client.view_project', project_id=project_id))

    amount_inr = float(accepted['bid_amount'])
    freelancer = {
        'first_name': accepted.get('freelancer_first', ''),
        'last_name': accepted.get('freelancer_last', '')
    }

    return render_template('payment/initiate.html',
                           project=project,
                           amount=amount_inr,
                           freelancer=freelancer,
                           razorpay_key_id=current_app.config['RAZORPAY_KEY_ID'])


@payment_bp.route('/create_order', methods=['POST'])
@login_required
def create_order():
    if session.get('role') != 'client':
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.get_json() or {}
    project_id = data.get('project_id')
    amount = data.get('amount')

    if not project_id or not amount:
        return jsonify({'error': 'Missing parameters'}), 400

    project = ProjectModel.get_by_id(project_id)
    if not project or project['client_id'] != session['user_id']:
        return jsonify({'error': 'Forbidden'}), 403

    # Proposal accepted — double check bid amount range
    from app.models.proposal import ProposalModel
    proposals = ProposalModel.get_by_project(project_id)
    accepted  = next((p for p in proposals if p['status'] == 'accepted'), None)
    if not accepted:
        return jsonify({'error': 'No accepted proposal found.'}), 400

    amount_inr = float(amount)
    amount_paise = int(amount_inr * 100)

    try:
        client = get_razorpay_client()
        order = client.order.create({
            'amount':   amount_paise,
            'currency': 'INR',
            'receipt':  f'proj_{project_id}',
            'notes':    {'project_id': project_id},
        })
        payment_id = PaymentModel.create_order(
            project_id, session['user_id'],
            project['hired_freelancer_id'],
            amount_inr, order['id']
        )
        return jsonify({
            'order_id': order['id'],
            'amount': amount_paise,
            'payment_db_id': payment_id
        })
    except Exception as ex:
        current_app.logger.error(f"Create order API error: {ex}")
        return jsonify({'error': 'Payment gateway error.'}), 500


# ── Verify Payment ────────────────────────────────────────────
@payment_bp.route('/verify', methods=['POST'])
@login_required
def verify():
    razorpay_order_id   = request.form.get('razorpay_order_id')
    razorpay_payment_id = request.form.get('razorpay_payment_id')
    razorpay_signature  = request.form.get('razorpay_signature')
    payment_db_id       = request.form.get('payment_db_id', type=int)

    # Verify signature
    secret    = current_app.config['RAZORPAY_KEY_SECRET']
    body      = f"{razorpay_order_id}|{razorpay_payment_id}"
    generated = hmac.new(secret.encode(), body.encode(), hashlib.sha256).hexdigest()

    if generated == razorpay_signature:
        PaymentModel.complete_payment(payment_db_id, razorpay_payment_id, razorpay_signature)
        PaymentModel.add_transaction(payment_db_id, 'payment',
                                     PaymentModel.get_by_id(payment_db_id)['amount'],
                                     'Razorpay payment received')
        # Mark project completed
        payment = PaymentModel.get_by_id(payment_db_id)
        if payment:
            ProjectModel.update_status(payment['project_id'], 'completed')
            NotificationModel.create(
                payment['freelancer_id'], 'payment_success',
                'Payment Received!',
                f"Payment of ₹{payment['amount']} received for project: {payment['project_title']}",
                link=url_for('payment.history')
            )
        flash('Payment successful! Project marked as completed.', 'success')
        return redirect(url_for('payment.invoice', payment_id=payment_db_id))
    else:
        PaymentModel.fail_payment(payment_db_id)
        flash('Payment verification failed. Please contact support.', 'danger')
        return redirect(url_for('payment.history'))


# ── Payment History ───────────────────────────────────────────
@payment_bp.route('/history')
@login_required
def history():
    payments = PaymentModel.get_history(session['user_id'], session['role'])
    return render_template('payment/history.html', payments=payments)


# ── Invoice ───────────────────────────────────────────────────
@payment_bp.route('/invoice/<int:payment_id>')
@login_required
def invoice(payment_id):
    payment = PaymentModel.get_by_id(payment_id)
    if not payment:
        abort(404)
    if payment['client_id'] != session['user_id'] and \
       payment['freelancer_id'] != session['user_id']:
        abort(403)
    return render_template('payment/invoice.html', payment=payment)


@payment_bp.route('/invoice/<int:payment_id>/download')
@login_required
def download_invoice(payment_id):
    """Generate a simple PDF invoice using reportlab."""
    payment = PaymentModel.get_by_id(payment_id)
    if not payment:
        abort(404)
    if payment['client_id'] != session['user_id'] and \
       payment['freelancer_id'] != session['user_id']:
        abort(403)

    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        import io

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        w, h = letter

        # Header
        c.setFont("Helvetica-Bold", 22)
        c.drawString(50, h - 60, "Freelance Marketplace")
        c.setFont("Helvetica", 12)
        c.drawString(50, h - 80, "Invoice / Receipt")

        c.line(50, h - 90, w - 50, h - 90)

        y = h - 130
        fields = [
            ("Invoice #",        f"INV-{payment['id']:06d}"),
            ("Project",          payment.get('project_title', '')),
            ("Client",           f"{payment['client_first']} {payment['client_last']}"),
            ("Freelancer",       f"{payment['freelancer_first']} {payment['freelancer_last']}"),
            ("Amount",           f"INR {payment['amount']}"),
            ("Status",           payment['status'].capitalize()),
            ("Payment ID",       payment.get('razorpay_payment_id', 'N/A')),
            ("Date",             str(payment['created_at'])),
        ]
        for label, value in fields:
            c.setFont("Helvetica-Bold", 11)
            c.drawString(50, y, f"{label}:")
            c.setFont("Helvetica", 11)
            c.drawString(200, y, str(value))
            y -= 25

        c.showPage()
        c.save()
        buffer.seek(0)

        response = make_response(buffer.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            f'attachment; filename=invoice_{payment_id}.pdf'
        return response
    except Exception as ex:
        current_app.logger.error(f"Invoice PDF error: {ex}")
        flash('Could not generate PDF. View online invoice instead.', 'warning')
        return redirect(url_for('payment.invoice', payment_id=payment_id))
