#!/usr/bin/env python3
"""
Module for Session Authentication View
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth
from api.v1.auth.session_auth import SessionAuth


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    """
    Handle user login using session authentication
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Ensure that auth object is an instance of SessionAuth
    if not isinstance(auth, SessionAuth):
        return jsonify({"error": "authentication mechanism not supported"}), 500

    session_id = auth.create_session(user[0].id)
    user_json = user[0].to_json()
    response = jsonify(user_json)
    response.set_cookie(auth.session_cookie_name, session_id)

    return response
