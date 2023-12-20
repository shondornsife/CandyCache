from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.model_user import User
from flask_app.models.model_candy import Candy


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/dashboard")
    return render_template("index.html")


# DISPLAY ROUTE shows the form of dashboard
@app.route("/dashboard")
def dashboard():
    if not "user_id" in session:
        return redirect("/")
    user = User.get_one({"id": session["user_id"]})
    all_candies = Candy.get_all()
    return render_template("dashboard.html", user=user, all_candies=all_candies)


@app.route("/logout")
def logout():
    # Clear the session to log the user out
    session.clear()
    return redirect("/")
