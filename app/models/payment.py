"""
Payment model — Razorpay orders, payments, transactions.
"""
from database import execute_query


class PaymentModel:

    @staticmethod
    def create_order(project_id, client_id, freelancer_id, amount, razorpay_order_id):
        return execute_query(
            """INSERT INTO payments
               (project_id, client_id, freelancer_id, amount, razorpay_order_id, status)
               VALUES (%s,%s,%s,%s,%s,'pending')""",
            (project_id, client_id, freelancer_id, amount, razorpay_order_id),
            fetch='none', commit=True
        )

    @staticmethod
    def complete_payment(payment_id, razorpay_payment_id, razorpay_signature):
        execute_query(
            """UPDATE payments SET status='completed',
               razorpay_payment_id=%s, razorpay_signature=%s
               WHERE id=%s""",
            (razorpay_payment_id, razorpay_signature, payment_id),
            fetch='none', commit=True
        )

    @staticmethod
    def fail_payment(payment_id):
        execute_query(
            "UPDATE payments SET status='failed' WHERE id=%s",
            (payment_id,), fetch='none', commit=True
        )

    @staticmethod
    def refund_payment(payment_id, refund_id):
        execute_query(
            "UPDATE payments SET status='refunded', refund_id=%s WHERE id=%s",
            (refund_id, payment_id), fetch='none', commit=True
        )

    @staticmethod
    def get_by_id(payment_id):
        return execute_query(
            """SELECT pay.*, p.title AS project_title,
                      uc.first_name AS client_first, uc.last_name AS client_last,
                      uf.first_name AS freelancer_first, uf.last_name AS freelancer_last
               FROM payments pay
               JOIN projects p ON p.id=pay.project_id
               JOIN users uc ON uc.id=pay.client_id
               JOIN users uf ON uf.id=pay.freelancer_id
               WHERE pay.id=%s""",
            (payment_id,), fetch='one'
        )

    @staticmethod
    def get_by_order_id(razorpay_order_id):
        return execute_query(
            "SELECT * FROM payments WHERE razorpay_order_id=%s",
            (razorpay_order_id,), fetch='one'
        )

    @staticmethod
    def get_history(user_id, role):
        field = 'client_id' if role == 'client' else 'freelancer_id'
        return execute_query(
            f"""SELECT pay.*, p.title AS project_title,
                       uc.first_name AS client_first, uc.last_name AS client_last,
                       uf.first_name AS freelancer_first, uf.last_name AS freelancer_last
                FROM payments pay
                JOIN projects p ON p.id=pay.project_id
                JOIN users uc ON uc.id=pay.client_id
                JOIN users uf ON uf.id=pay.freelancer_id
                WHERE pay.{field}=%s
                ORDER BY pay.created_at DESC""",
            (user_id,), fetch='all'
        )

    @staticmethod
    def add_transaction(payment_id, type_, amount, note=''):
        execute_query(
            "INSERT INTO transactions (payment_id,type,amount,note) VALUES (%s,%s,%s,%s)",
            (payment_id, type_, amount, note), fetch='none', commit=True
        )

    @staticmethod
    def get_total_earnings(freelancer_id):
        row = execute_query(
            """SELECT COALESCE(SUM(amount),0) AS total
               FROM payments
               WHERE freelancer_id=%s AND status='completed'""",
            (freelancer_id,), fetch='one'
        )
        return row['total'] if row else 0

    @staticmethod
    def get_by_project(project_id):
        return execute_query(
            "SELECT * FROM payments WHERE project_id=%s ORDER BY created_at DESC LIMIT 1",
            (project_id,), fetch='one'
        )
