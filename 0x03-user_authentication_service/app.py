#!/usr/bin/env python3
"""
Flask App Module
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def index():
    """Index route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a new user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")

        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    """Login route"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)

    if not session_id:
        abort(401)

    # Create a response with JSON payload
    response = jsonify({"email": email, "message": "logged in"})
    # Set the session_id as a cookie in the response
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logout a user by destroying the session."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        AUTH.destroy_session(user.id)
        return redirect("/")
    else:
        return jsonify({"message": "Forbidden"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
