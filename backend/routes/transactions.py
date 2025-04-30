from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend.models import db, BorrowTransactions, BookCopies, Users, BookRenewals, Fines, Reservations

transactions = Blueprint("transactions", __name__, url_prefix="/transactions")


# Borrow a book
@transactions.route("/borrow", methods=["POST"])
@jwt_required()
def borrow_book():
    data = request.json
    user_id = get_jwt_identity()
    book_id = data.get("book_id")  # Instead of copy_id, get book_id
    reservation_id = data.get("reservation_id")

    user = Users.query.get(user_id)
    copy = BookCopies.query.filter_by(book_id=book_id, is_borrowed=False).first()

    if not copy:
        return jsonify({"error": "No copies to borrow"}), 404

    # Enforce borrowing limit
    borrow_count = BorrowTransactions.query.filter_by(user_id=user_id, is_returned=False).count()
    borrow_limit = 3 if user.user_type == "student" else 5

    if borrow_count >= borrow_limit:
        return jsonify({"error": "Borrowing limit reached"}), 400

    # Set due date
    due_days = 14 if user.user_type == "student" else 30
    due_date = datetime.now(timezone.utc) + timedelta(days=due_days)

    transaction = BorrowTransactions(
        user_id=user_id,
        copy_id=copy.id,
        issue_date=datetime.now(timezone.utc),
        due_date=due_date,
        is_returned=False,
        fine=0.0
    )

    copy.is_borrowed = True

    if reservation_id:
        reservation = Reservations.query.filter_by(id=reservation_id).first()
        if reservation and reservation.user_id == user_id and reservation.status == "pending":
            reservation.status = "borrowed"
            db.session.add(reservation)

    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Book borrowed successfully", "transaction_id": transaction.id,
                    "due_date": due_date.strftime('%Y-%m-%d')})


# Return a book
@transactions.route("/return", methods=["POST"])
@jwt_required()
def return_book():
    data = request.json
    transaction_id = data.get("transaction_id")

    transaction = BorrowTransactions.query.get(transaction_id)
    if not transaction or transaction.is_returned:
        return jsonify({"error": "Invalid transaction"}), 400

    # Check if overdue
    overdue_days = (datetime.now(timezone.utc) - datetime.combine(transaction.due_date, datetime.min.time(),
                                                                  timezone.utc)).days
    fine_amount = max(0, overdue_days * 10)  # Example: ₹10/- per day

    transaction.is_returned = True
    transaction.fine = fine_amount

    # Update book availability
    copy = BookCopies.query.get(transaction.copy_id)
    copy.is_borrowed = False

    # Save f#ine if applicable
    if fine_amount > 0:
        fine_entry = Fines(user_id=transaction.user_id, amount=fine_amount, paid=False)
        db.session.add(fine_entry)

    db.session.commit()

    return jsonify({"message": "Book returned successfully", "fine": fine_amount})


@transactions.route("/pay_fine", methods=["POST"])
@jwt_required()
def pay_fine():
    data = request.json
    fine_id = data.get("fine_id")

    fine = Fines.query.get(fine_id)
    if not fine or fine.paid:
        return jsonify({"error": "Invalid fine"}), 400

    fine.paid = True
    db.session.commit()

    return jsonify({"message": "Fine paid successfully"})


@transactions.route("/renew", methods=["POST"])
@jwt_required()
def renew_book():
    data = request.json
    transaction_id = data.get("transaction_id")

    transaction = BorrowTransactions.query.get(transaction_id)
    if not transaction or transaction.is_returned:
        return jsonify({"error": "Invalid transaction"}), 400

    # Extend due date
    renewal_days = 14  # Fixed renewal period
    new_due_date = transaction.due_date + timedelta(days=renewal_days)

    renewal = BookRenewals(transaction_id=transaction.id, renewal_date=datetime.now(timezone.utc))

    transaction.due_date = new_due_date

    db.session.add(renewal)
    db.session.commit()

    return jsonify({"message": "Book renewed successfully", "new_due_date": new_due_date.strftime('%Y-%m-%d')})
