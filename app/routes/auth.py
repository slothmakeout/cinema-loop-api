from flask import Blueprint, jsonify, request
from passlib.hash import bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from app import db
from app.models import Account

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    login = data.get("login")
    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    bio = data.get("bio")

    if not login or not email or not password:
        return jsonify({"msg": "Login, email, and password are required"}), 400

    if Account.query.filter(
        (Account.login == login) | (Account.email == email)
    ).first():
        return jsonify({"msg": "User with this login or email already exists"}), 400

    password_hash = bcrypt.hash(password)
    new_account = Account(
        login=login,
        email=email,
        password_hash=password_hash,
        first_name=first_name,
        last_name=last_name,
        bio=bio,
    )

    db.session.add(new_account)
    db.session.commit()

    return jsonify({"msg": "Registration successful"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    login = data.get("login")
    password = data.get("password")

    if not login or not password:
        return jsonify({"msg": "Login and password are required"}), 400

    account = Account.query.filter_by(login=login).first()

    if not account or not account.verify_password(password):
        return jsonify({"msg": "Invalid login or password"}), 401

    access_token = create_access_token(
        identity=account.id, expires_delta=timedelta(weeks=1)
    )
    return jsonify({"access_token": access_token}), 200
