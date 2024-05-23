from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Account

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/accounts", methods=["GET"])
@jwt_required()
def get_accounts():
    current_user_id = get_jwt_identity()
    accounts = Account.query.all()
    accounts_list = [account.to_dict() for account in accounts]
    return jsonify({"accounts": accounts_list, "current_user_id": current_user_id})


@profile_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    current_user_id = get_jwt_identity()
    account = Account.query.get(current_user_id)
    if not account:
        return jsonify({"msg": "User not found"}), 404
    return jsonify(account.to_dict()), 200
