from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash 
from flask_app import app
from flask_app.models import users

class Painting:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']

    @staticmethod
    def validate_painting(form_data):
        is_valid = True 

        if len(form_data["title"]) <2:
            flash("Title must be at least 2 characters long!")
            is_valid = False
        if len(form_data["description"]) <10:
            flash("Description must be at least 10 characters long!")
            is_valid = False
        if len(form_data["price"]) <0:
            flash("Price must be greater than $0 and answer must include $!")
            is_valid = False

        return is_valid

    @classmethod
    def save_painting(cls, data ):
        query = "INSERT INTO paintings ( title , description , price , created_at, updated_at, users_id ) VALUES ( %(title)s , %(description)s , %(price)s , NOW() , NOW(), %(users_id)s );"
        # data is a dictionary that will be passed into the save method from server.py

        return connectToMySQL('paintings_schema').query_db( query, data )

    @classmethod
    def get_one_painting(cls, data):
        query = "SELECT * FROM paintings WHERE paintings.id = %(id)s;"
        results = connectToMySQL('paintings_schema').query_db(query,data)

        painting = cls(results[0])

        return painting

    @classmethod
    def get_all_paintings_with_users(cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.users_id = users.id;"

        results = connectToMySQL("paintings_schema").query_db(query)

        all_paintings =[]

        for row in results:
            one_painting = cls(row)

            user_data ={
                "id" : row["users.id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "created_at" : row["users.created_at"],
                "updated_at" : row["users.updated_at"],
            }
            one_painting.user = users.User(user_data)
            all_paintings.append(one_painting)
        return all_paintings

    @classmethod
    def get_one_painting_with_user(cls, data):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.users_id = users.id WHERE paintings.id = %(id)s;"
        results = connectToMySQL("paintings_schema").query_db(query, data)

        painting = cls(results[0])

        user_data ={
                "id" : results[0]["users.id"],
                "first_name" : results[0]["first_name"],
                "last_name" : results[0]["last_name"],
                "email" : results[0]["email"],
                "password" : results[0]["password"],
                "created_at" : results[0]["users.created_at"],
                "updated_at" : results[0]["users.updated_at"],
            }
        painting.user = users.User(user_data)
        return painting


    @classmethod
    def edit_painting_info(cls,data):
        query = "UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, updated_at = NOW() WHERE id=%(id)s;"

        results = connectToMySQL("paintings_schema").query_db(query, data)
        return

    @classmethod
    def delete_one_painting(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"

        results = connectToMySQL("paintings_schema").query_db(query, data)
        return 