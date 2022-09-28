# Remember to do ALL applicable imports
from sqlite3 import connect
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# For bcrypt
from flask_app import app # Import the app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Link models as needed in your projects
from flask_app.models import user

class Car:
    database_name = "users_car_deals_schema" # class variable holding the schema 
    def __init__(self, data): # data is a dictionary representing a record which is also a row from the database
        self.id = data["id"] # need to be sure that the names match the columns in the database
        self.price = data["price"]
        self.model = data["model"]
        self.make = data["make"]
        self.year = data["year"]
        self.description = data["description"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = None # creating placeholder to hold a single user value since a car can only have 1 user. You can pick any name here and user was picked


    # Class method to add cars to the database
    @classmethod
    def add_car(cls, data):
        query = "INSERT INTO cars (price, model, make, year, description, user_id) VALUES (%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(user_id)s);"
        return connectToMySQL(cls.database_name).query_db(query, data)


    # Get all cars with the users who added it
    @classmethod
    def get_all_cars_with_users(cls):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id;"
        output = connectToMySQL(cls.database_name).query_db(query)
        print(output)
        if len(output) == 0:
            return []
        else:
            all_car_list = [] # will store all cars
            # Loop through each car from the query by going through each dictionary
            for current_car_dict in output:
                # Create a car or class instance
                car_inst= cls(current_car_dict)
                # Get the info about the user who is selling the car and place it in another dictionary
                new_user_dict = {
                    "id": current_car_dict["users.id"],
                    "first_name": current_car_dict["first_name"],
                    "last_name": current_car_dict["last_name"],
                    "email": current_car_dict["email"],
                    "password": current_car_dict["password"],
                    "created_at": current_car_dict["users.created_at"],
                    "updated_at": current_car_dict["users.updated_at"]
                }
                # Create the user class instance
                user_inst = user.User(new_user_dict)
                # Link this user to the car being sold
                car_inst.user = user_inst
                # Add the car to the list called all_car_list
                all_car_list.append(car_inst)
            return all_car_list


    # Get one car with info on user who added it
    @classmethod
    def get_one_car_with_user(cls, data):
        query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        output = connectToMySQL(cls.database_name).query_db(query, data)
        print(output)
        if len(output) == 0:
            return []
        else:
            # create a class instance of the car
            car_inst = cls(output[0])
            # Get the user info on who added the car and will place it in another new dictionary
            new_car_dict = {
                "id": output[0]["users.id"],
                "first_name": output[0]["first_name"],
                "last_name": output[0]["last_name"],
                "email": output[0]["email"],
                "password": output[0]["password"],
                "created_at": output[0]["users.created_at"],
                "updated_at": output[0]["users.updated_at"],
            }
            # Create the class instance of User
            user_inst = user.User(new_car_dict)
            # Linking user to the car
            car_inst.user = user_inst
            return car_inst


    # Edit car info
    @classmethod
    def edit_car(cls, data):
        query = "UPDATE cars SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query, data)


    # Delete car info
    @classmethod
    def delete_car(cls, data):
        query = "DELETE FROM cars WHERE id = %(id)s;"
        return connectToMySQL(cls.database_name).query_db(query, data)





    # Validations are done here
    @staticmethod
    def validate_car(car_info):
        is_valid = True
        print(car_info) # printing to terminal to see output
        # Checking length of the name
        if int(car_info['price']) < 1:
            is_valid = False
            flash("Price must be greater than 0.", "car")
        if car_info["model"] == '':
            is_valid = False
            flash("Model is a required field.", "car")
        if car_info["make"] == '':
            is_valid = False
            flash("Make is a required field.", "car")
        if int(car_info['year']) < 1:
            is_valid = False
            flash("Year must be greater than 0.", "car")
        if car_info["description"] == '':
            is_valid = False
            flash("Description is a required field.", "car")
        return is_valid