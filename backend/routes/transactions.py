from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from backend.models import db, BorrowTransactions, BookCopies, Users, BookRenewals, Fines, Reservations, Books
from backend.utils import is_admin

transactions = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions.route("/", methods=["GET"])
@jwt_required()
def borrow_transactions():
    if not is_admin():
        return jsonify({"status": "error", "message": "You are not admin!"}), 401

    try:
        all_transactions = BorrowTransactions.query.all()
        if not all_transactions:
            return jsonify({"status": "error", "message": "There are no transactions!"}), 404

        result = []
        for res in all_transactions:
            copy = BookCopies.query.get(res.copy_id)
            book = Books.query.get(copy.book_id) if copy else None
            user = Users.query.get(res.user_id)
            result.append({
                "transaction_id": res.id,
                "book_name": book.title if book else "Unknown",
                "book_author": book.author if book else "Unknown",
                "user_email": user.email if user else "Unknown",
                "is_returned": res.is_returned,
                "is_overdue": datetime.now(timezone.utc).date() > res.due_date if not res.is_returned else False,
                "fine": res.fine,
                "fine_status": (
                    Fines.query.filter_by(transaction_id=res.id).first().status
                    if Fines.query.filter_by(transaction_id=res.id).first()
                    else "none"
                )
            })

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500

# Borrow a book
@transactions.route("/borrow", methods=["POST"])
@jwt_required()
def borrow_book():
    try:
        data = request.json
        if not is_admin():
            return jsonify({"status": "error", "message": "Not authorized"}), 401

        user_id = data.get("user_id")
        book_id = data.get("book_id")  # Instead of copy_id, get book_id
        reservation_id = data.get("reservation_id")

        user = Users.query.get(user_id)
        copy = BookCopies.query.filter_by(book_id=book_id, is_borrowed=False).first()

        if not user:
            return jsonify({"status": "error", "message": "Unknown User"}), 404

        if not copy:
            return jsonify({"status": "error", "message": "No copies available to borrow"}), 404

        # Enforce borrowing limit
        borrow_count = BorrowTransactions.query.filter_by(user_id=user_id, is_returned=False).count()
        borrow_limit = 3 if user.user_type == "student" else 5

        if borrow_count >= borrow_limit:
            return jsonify({"status": "error", "message": "Borrowing limit reached"}), 400

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

        return jsonify({
            "status": "success",
            "message": "Book borrowed successfully",
            "data": {
                "transaction_id": transaction.id,
                "due_date": due_date.strftime('%Y-%m-%d')
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Failed to borrow book"}), 500


# Return a book
@transactions.route("/return", methods=["POST"])
@jwt_required()
def return_book():
    try:
        data = request.json
        transaction_id = data.get("transaction_id")

        if not transaction_id:
            return jsonify({"status": "error", "message": "Transaction ID is required"}), 400

        transaction = BorrowTransactions.query.get(transaction_id)
        if not transaction:
            return jsonify({"status": "error", "message": "Transaction not found"}), 404

        if transaction.is_returned:
            return jsonify({"status": "error", "message": "Book already returned"}), 400

        # Check if overdue
        overdue_days = (datetime.now(timezone.utc) - datetime.combine(transaction.due_date, datetime.min.time(),
                                                                      timezone.utc)).days
        fine_amount = max(0, overdue_days * 10)

        transaction.is_returned = True
        transaction.return_date = datetime.now(timezone.utc)
        transaction.fine = fine_amount

        # Update book availability
        copy = BookCopies.query.get(transaction.copy_id)
        if copy:
            copy.is_borrowed = False

        # Save fine if applicable
        if fine_amount > 0:
            fine_entry = Fines(
                user_id=transaction.user_id,
                transaction_id=transaction.id,
                amount=fine_amount,
                status="unpaid"
            )
            db.session.add(fine_entry)

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Book returned successfully",
            "data": {
                "fine": fine_amount,
                "transaction_id": transaction.id
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status": "error", "message": "Failed to return book"}), 500


@transactions.route("/payfine", methods=["POST"])
@jwt_required()
def pay_fine():
    try:
        data = request.json
        transaction_id = data.get("transaction_id")

        if not transaction_id:
            return jsonify({"status": "error", "message": "Transaction ID is required"}), 400

        # Find unpaid fine by transaction_id
        fine = Fines.query.filter_by(transaction_id=transaction_id, status="unpaid").first()

        if not fine:
            return jsonify({"status": "error", "message": "No unpaid fine found for this transaction"}), 404

        # Mark fine as paid
        fine.status = "paid"
        fine.payment_date = datetime.now(timezone.utc)

        # Update transaction's fine_paid field
        transaction = BorrowTransactions.query.get(transaction_id)
        if transaction:
            transaction.fine_paid = True

        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Fine paid successfully",
            "data": {
                "fine_id": fine.id,
                "amount": fine.amount
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({"status": "error", "message": "Failed to pay fine"}), 500

@transactions.route("/renew", methods=["POST"])
@jwt_required()
def renew_book():
    try:
        data = request.json
        transaction_id = data.get("transaction_id")

        if not transaction_id:
            return jsonify({"status": "error", "message": "Transaction ID is required"}), 400

        transaction = BorrowTransactions.query.get(transaction_id)
        if not transaction:
            return jsonify({"status": "error", "message": "Transaction not found"}), 404

        if transaction.is_returned:
            return jsonify({"status": "error", "message": "Cannot renew returned book"}), 400

        # Check if book is already overdue
        if datetime.now(timezone.utc).date() > transaction.due_date:
            return jsonify({"status": "error", "message": "Cannot renew overdue book"}), 400

        # Check renewal limit
        renewal_count = BookRenewals.query.filter_by(transaction_id=transaction.id).count()
        if renewal_count >= 2:  # Max 2 renewals
            return jsonify({"status": "error", "message": "Maximum renewal limit reached"}), 400

        # Extend due date
        renewal_days = 14  # Fixed renewal period
        new_due_date = transaction.due_date + timedelta(days=renewal_days)

        renewal = BookRenewals(
            transaction_id=transaction.id,
            renewal_date=datetime.now(timezone.utc)
        )

        transaction.due_date = new_due_date

        db.session.add(renewal)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": "Book renewed successfully",
            "data": {
                "new_due_date": new_due_date.strftime('%Y-%m-%d'),
                "renewals_remaining": 2 - renewal_count - 1
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": "Failed to renew book"}), 500


# Get user transactions
@transactions.route("/user/<string:email>", methods=["GET"])
@jwt_required()
def user_transactions(email):
    if not is_admin():
        return jsonify({"status": "error", "message": "You are not admin!"}), 401

    try:
        user = Users.query.filter_by(email=email).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        transactions = BorrowTransactions.query.filter_by(user_id=user.id).all()

        if not transactions:
            return jsonify({"status": "success", "data": []}), 200

        result = []
        for res in transactions:
            copy = BookCopies.query.get(res.copy_id)
            book = Books.query.get(copy.book_id) if copy else None
            result.append({
                "transaction_id": res.id,
                "book_name": book.title if book else "Unknown",
                "book_author": book.author if book else "Unknown",
                "user_email": user.email,
                "is_returned": res.is_returned,
                "is_overdue": datetime.now(timezone.utc).date() > res.due_date if not res.is_returned else False,
                "fine": res.fine,
                "fine_status": (
                    Fines.query.filter_by(transaction_id=res.id).first().status
                    if Fines.query.filter_by(transaction_id=res.id).first()
                    else "none"
                )
            })

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500


# NEW: Get all fines for a user
@transactions.route("/fines/user/<string:user_email>", methods=["GET"])
@jwt_required()
def get_user_fines(user_email):
    try:
        if not is_admin():
            return jsonify({"status": "error", "message": "Not authorized"}), 401

        user = Users.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({"status": "error", "message": "User not found"}), 404

        # Get all fines for the user
        fines_query = Fines.query.filter_by(user_id=user.id).order_by(
            Fines.created_at.desc()
        )

        result = []
        total_unpaid = 0

        for fine in fines_query:
            # Get transaction details if available
            transaction = None
            book_info = None

            if fine.transaction_id:
                transaction = BorrowTransactions.query.get(fine.transaction_id)
                if transaction:
                    copy = BookCopies.query.get(transaction.copy_id)
                    if copy:
                        book = Books.query.filter_by(isbn=copy.book_id).first()
                        if book:
                            book_info = {
                                "title": book.title,
                                "author": book.author,
                                "isbn": book.isbn
                            }

            fine_data = {
                "fine_id": fine.id,
                "transaction_id": fine.transaction_id,
                "amount": float(fine.amount),
                "status": fine.status,
                "created_at": fine.created_at.strftime("%Y-%m-%d %H:%M:%S") if fine.created_at else None,
                "payment_date": fine.payment_date.strftime("%Y-%m-%d %H:%M:%S") if fine.payment_date else None,
                "book_info": book_info,
                "reason": "Overdue return" if transaction else "Other"
            }

            if fine.status == "unpaid":
                total_unpaid += float(fine.amount)

            result.append(fine_data)

        return jsonify({
            "status": "success",
            "data": {
                "fines": result,
                "total_fines": len(result),
                "total_unpaid_amount": total_unpaid,
                "unpaid_count": len([f for f in result if f["status"] == "unpaid"])
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to fetch fines"}), 500


# NEW: Get fine statistics
@transactions.route("/fines/stats", methods=["GET"])
@jwt_required()
def get_fine_stats():
    try:
        if not is_admin():
            return jsonify({"status": "error", "message": "Not authorized"}), 401

        # Get overall fine statistics
        total_fines = Fines.query.count()
        unpaid_fines = Fines.query.filter_by(status="unpaid").count()
        paid_fines = Fines.query.filter_by(status="paid").count()

        total_unpaid_amount = db.session.query(db.func.sum(Fines.amount)).filter_by(status="unpaid").scalar() or 0
        total_paid_amount = db.session.query(db.func.sum(Fines.amount)).filter_by(status="paid").scalar() or 0

        return jsonify({
            "status": "success",
            "data": {
                "total_fines": total_fines,
                "unpaid_fines": unpaid_fines,
                "paid_fines": paid_fines,
                "total_unpaid_amount": float(total_unpaid_amount),
                "total_paid_amount": float(total_paid_amount),
                "collection_rate": round((paid_fines / total_fines * 100), 2) if total_fines > 0 else 0
            }
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": "Failed to fetch fine statistics"}), 500
