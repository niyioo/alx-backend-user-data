#!/usr/bin/env python3
"""
Flask App Module
"""
from flask import Flask, jsonify, request, redirect, abort
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
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


@app.route("/profile", methods=["GET"])
def profile():
    """Retrieve user profile."""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        return "Forbidden", 403


@app.route("/reset_password", methods=["POST"])
def get_reset_password_token():
    """Generate a reset password token."""
    # Get the email from the form data
    email = request.form.get("email")

    try:
        # Generate a reset password token
        reset_token = auth.get_reset_password_token(email)

        # Respond with a JSON payload containing the email and reset token
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        # If the email is not registered, respond with a 403 status code
        abort(403)


@app.route("/reset_password", methods=["PUT"])
def update_password():
    """Update user's password"""
    try:
        email = request.form.get("email")
        reset_token = request.form.get("reset_token")
        new_password = request.form.get("new_password")

        # Update the password
        AUTH.update_password(reset_token, new_password)

        # Respond with success message
        return jsonify({"email": email, "message": "Password updated"}), 200
    except ValueError:
        # If the token is invalid, respond with a 403 HTTP code
        return jsonify({"message": "Invalid token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
