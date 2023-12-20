from flask_app import app, bcrypt
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_user import User


# DISPLAY ROUTE - shows the form to create users
@app.route("/users/new")
def users_new():
    return render_template("index.html")


# ACTION ROUTE - process the form from the new route (above)
@app.post("/register")
def submit_form():
    print(request.form)
    is_valid = User.validate(request.form)

    if not is_valid:
        return redirect("/")

    hash_pw = bcrypt.generate_password_hash(request.form["password"])
    print(hash_pw)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hash_pw,
    }

    session["first_name"] = request.form["first_name"]
    session["last_name"] = request.form.get("last_name")
    session["email"] = request.form.get("email")
    # Call the save @classmethod on User
    user_id = User.create(data)
    # store user id into session
    session["user_id"] = user_id
    return redirect("/dashboard")


# Login Session
@app.post("/login")
def login_process():
    is_valid = User.validator_login(request.form)

    if not is_valid:
        return redirect("/")
    # User.validator_login(request.form)
    # if request.method == "POST":
    #     session["email"] = request.form["email"]
    #     if not User.validator_login(request.form):
    #         return redirect("/")

    #     # see if the username provided exists in the database
    #     data = {"email": request.form["email"]}
    #     user_in_db = User.get_one_by_email(data)

    #     if user_in_db is not None:
    #         print(user_in_db.password)
    #         if not bcrypt.check_password_hash(
    #             user_in_db.password, request.form["password"]
    #         ):
    #             flash("Invalid Password", "err_users_loginpassword")
    #             return redirect("/")
    #         # if the passwords matched, we set the user_id into session
    #         session["user_id"] = user_in_db.id
    #         return redirect("/dashboard")
    #     else:
    #         flash("Invalid Email", "err_users_loginemail")
    return redirect("/dashboard")


# DISPLAY ROUTE - just display the users info
@app.route("/users/<int:id>")
def users_show(id):
    # get the users from the database and pass that instance of the users to the html page
    return render_template("index.html")


# DISPLAY ROUTE - display the form to edit the users
@app.route("/user/<int:id>/edit")
def users_edit(id):
    if "user_id" not in session:
        return redirect("/")

    # get the users from the database and pass that instance of the users to the html page
    return render_template("users_edit.html")


# ACTION ROUTE - process the form from the edit route
@app.route("/users/<int:id>/update")
def users_update(id):
    if "user_id" not in session:
        return redirect("/")
    # in the future make sure that the user is supposed to be able to update the record
    # using the id that come in update the record
    return redirect("/")


# ACTION ROUTE - delete the record from the database
@app.post("/user/<int:id>/delete")
def users_delete(id):
    if "user_id" not in session:
        return redirect("/")
    # call on the delete method from the class to delete the row in the database
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
