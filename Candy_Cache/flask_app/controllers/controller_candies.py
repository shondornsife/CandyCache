from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.model_candy import Candy
from flask_app.models.model_user import User


@app.route("/candies/<int:id>")
def candies_show(id):
    if "user_id" not in session:
        return redirect("/")
    candy = Candy.get_one({"id": id})
    return render_template("candies_show.html", candy=candy)


@app.route("/candies/new")
def candies_new():
    if "user_id" not in session:
        return redirect("/")
    user = User.get_one({"id": session["user_id"]})
    return render_template("candies_new.html", user=user)


@app.route("/candies/create", methods=["POST"])
def candies_create():
    if "user_id" not in session:
        return redirect("/")
    if not Candy.validate(request.form):
        return redirect("/candies/new")

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "quantity": request.form["quantity"],
        "is_favorite": request.form.get("is_favorite"),
        "img_url": request.form["img_url"],
        "user_id": session["user_id"],
    }

    Candy.create(data)
    return redirect("/dashboard")


@app.route("/candies/<int:id>/edit")
def candies_edit(id):
    if "user_id" not in session:
        return redirect("/")

    user = User.get_one({"id": session["user_id"]})
    candy = Candy.get_one({"id": id})

    return render_template("candies_edit.html", user=user, candy=candy)


@app.route("/candies/<int:id>/update", methods=["POST"])
def candies_update(id):
    if "user_id" not in session:
        return redirect("/")

    if not Candy.validate(request.form):
        return redirect(f"/candies/{id}/edit")

    data = {
        "id": id,
        "name": request.form["name"],
        "description": request.form["description"],
        "quantity": request.form["quantity"],
        "is_favorite": request.form.get("is_favorite"),
        "img_url": request.form["img_url"],
        "user_id": session["user_id"],
    }

    Candy.update(data)

    # updated candy information
    updated_candy = Candy.get_one({"id": id})

    return render_template("candies_show.html", candy=updated_candy)


@app.route("/candies/<int:id>/delete")
def candies_delete(id):
    if "user_id" not in session:
        return redirect("/")
    Candy.delete_one({"id": id})
    return redirect("/dashboard")
