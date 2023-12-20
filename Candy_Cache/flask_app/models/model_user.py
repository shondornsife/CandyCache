from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
import re  # the regex module

# create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


class User:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # CREATE
    @classmethod
    def create(cls, data: dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

    # READ
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)

        if not results:
            return []

        instance_list = []
        for dict in results:
            instance_list.append(cls(dict))

        return instance_list

    @classmethod
    def get_one(cls, data: dict):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []

        dict = results[0]
        instance = cls(dict)
        return instance

    @classmethod
    def delete_one(cls, data: dict):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data: dict) -> bool:
        is_valid = True

        if len(data["first_name"]) < 2:
            flash("first name is required", "err_users_first_name")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("last name is required", "err_users_last_name")
            is_valid = False
        if len(data["email"]) < 7:
            flash(
                "email is required, must be at least 7 characters long",
                "err_users_email",
            )
            is_valid = False
        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address!", "err_users_email")
            is_valid = False
        else:
            potential_user = User.get_one_by_email(data)
            if potential_user:
                flash("Email address already exists!", "err_users_email")
                is_valid = False
        if len(data["password"]) < 8:
            flash(
                "password is required, must be at least 8 characters long",
                "err_users_password",
            )
            is_valid = False
        if len(data["confirm_password"]) < 8:
            flash(
                "confirm password is required, must be at least 8 characters long",
                "err_users_confirm_password",
            )
            is_valid = False
        elif data["password"] != data["confirm_password"]:
            flash(
                "password and confirm password do not match",
                "err_users_confirm_password",
            )
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validator_login(data: dict) -> bool:
        is_valid = True

        if len(data["email"]) < 7:
            flash("Invalid Email", "err_users_email")
            is_valid = False

        elif not EMAIL_REGEX.match(data["email"]):
            flash("Invalid email address", "err_users_loginemail")
            is_valid = False
        else:
            potential_user = User.get_one_by_email(data)
            if not potential_user:
                flash("Invalid credentials", "err_users_loginemail")
                is_valid = False
        if len(data["password"]) < 8:
            flash("Invalid credentials", "err_users_password")
            is_valid = False
        if is_valid:
            if not bcrypt.check_password_hash(
                potential_user.password, data["password"]
            ):
                flash("Invalid credentials", "err_users_password")
                is_valid = False
            else:
                session["user_id"] = potential_user.id
            return is_valid

    @classmethod
    def get_one_by_email(cls, data: dict):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return []

        dict = results[0]
        instance = cls(dict)
        return instance
