from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash
from flask_app.models.model_user import User


class Candy:
    def __init__(self, data: dict):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.quantity = data["quantity"]
        self.is_favorite = data["is_favorite"]
        self.img_url = data["img_url"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.owner = None  # THIS WILL HOLD USER OBJECT LATER

    @classmethod
    def create(cls, data: dict) -> int:
        query = "INSERT INTO candies (name, description, quantity, is_favorite, img_url, user_id) VALUES (%(name)s, %(description)s, %(quantity)s, %(is_favorite)s, %(img_url)s, %(user_id)s);"
        id = connectToMySQL(DATABASE).query_db(query, data)
        return id

    @classmethod
    def get_all(cls):
        query = """
        SELECT * FROM candies
        JOIN users ON candies.user_id = users.id;
        """
        results = connectToMySQL(DATABASE).query_db(query)

        if not results:
            return []

        instance_list = []
        for dict in results:
            candy_instance = cls(dict)
            user_data = {
                "id": dict["users.id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": dict["password"],
                "created_at": dict["users.created_at"],
                "updated_at": dict["users.updated_at"],
            }
            user_instance = User(user_data)
            candy_instance.owner = user_instance
            instance_list.append(candy_instance)
        return instance_list

    @classmethod
    def get_one(cls, data: dict):
        query = """
        SELECT * FROM candies
        LEFT JOIN users ON candies.user_id = users.id
        WHERE candies.id = %(id)s;
        """
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return None

        dict = results[0]
        candy_instance = cls(dict)
        user_data = {
            "id": dict["users.id"],
            "first_name": dict["first_name"],
            "last_name": dict["last_name"],
            "email": dict["email"],
            "password": dict["password"],
            "created_at": dict["users.created_at"],
            "updated_at": dict["users.updated_at"],
        }
        user_instance = User(user_data)
        candy_instance.owner = user_instance
        return candy_instance

    @classmethod
    def delete_one(cls, data: dict):
        query = "DELETE FROM candies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data: dict):
        query = "UPDATE candies SET name=%(name)s, description=%(description)s, quantity=%(quantity)s, is_favorite=%(is_favorite)s, img_url=%(img_url)s WHERE id=%(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validate(data: dict) -> bool:
        is_valid = True

        if len(data["name"]) < 2:
            flash("Name is required", "err_candies_name")
            is_valid = False
        if len(data["description"]) < 2:
            flash("Description is required", "err_candies_description")
            is_valid = False
        if not data["quantity"]:
            flash("Quantity is required", "err_candies_quantity")
            is_valid = False

        return is_valid
