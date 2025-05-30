from flask import Blueprint, jsonify

from backend.models import db, Books, BookCopies, Users, Fines

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/', methods=['GET'])
def get_dashboard_stats():
    try:
        total_books = db.session.query(Books).count()
        books_issued = db.session.query(BookCopies).filter_by(is_borrowed=True).count()
        active_users = db.session.query(Users).filter_by(is_active=True).count()
        members = db.session.query(Users).count()
        fine_collected = db.session.query(db.func.sum(Fines.amount)).filter(Fines.status == 'paid').scalar() or 0.0

        stats = [
            {"title": "Total Books", "value": total_books},
            {"title": "Books Issued", "value": books_issued},
            {"title": "Active Users", "value": active_users},

            {"title": "Members", "value": members},
            {"title": "Fine Collected", "value": fine_collected}
        ]

        return jsonify({"success": True, "data": stats}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
