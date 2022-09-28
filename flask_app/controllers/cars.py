from flask_app import app # Import the app
# Add bcrypt for hashing passwords when registering
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash
from flask_app.models import user, car # importing the model files here

# VISIBLE ROUTES
@app.route("/new")
def new_car():
    # doing a check to see if user is not logged in and sending them to the login page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": session["user_id"],
    }
    return render_template("add_car.html", this_user = user.User.get_one_user_by_id(data)) # going to the html page and also creating a new variable to hold the current user that's logged in


@app.route("/edit/<int:id>")
def edit_car(id): # Need to remember to use id as a parameter since using a path variable within the route
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id,
    }
    return render_template("edit_car.html", this_car = car.Car.get_one_car_with_user(data))


# INVISIBLE ROUTES

@app.route("/cars/add_car_to_db", methods=["POST"])
def add_car_to_db():
        # doing a check to see if user is not logged in and sending them to the login page if they're not
    if "user_id" not in session:
        return redirect("/")
    # Doing validation checks on form input before processing the info
    if not car.Car.validate_car(request.form): # Referencing the static method here
        return redirect("/new") # Redirecting back to entering new car html
    else:
        # Adding the car to the database using the model
        data = {
            "price": request.form["price"],
            "model": request.form["model"],
            "make": request.form["make"],
            "year": request.form["year"],
            "description": request.form["description"],
            "user_id": session["user_id"], # Placing the current user_id in session in the user_id attribute
        }
        car.Car.add_car(data) # Calling the class method created in the model file 
        # redirect to the dashboard
        return redirect("/dashboard")


@app.route("/cars/<int:id>/edit_car_in_db", methods=["POST"])
def edit_car_in_db(id):
    # Doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    # doing validation checks on form input before processing the info
    if not car.Car.validate_car(request.form):
        return redirect(f"/edit/{id}")
    else:
        # Edit car in the db through the model
        data = {
            "price": request.form["price"],
            "model": request.form["model"],
            "make": request.form["make"],
            "year": request.form["year"],
            "description": request.form["description"],
            "id": id # this is the id of the relic and not the user
        }
        car.Car.edit_car(data)
        # redirecting to new route
        return redirect("/dashboard")


@app.route("/show/<int:id>")
def view_car_info(id):
    # Doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    return render_template("view_car.html", this_car = car.Car.get_one_car_with_user(data))


# Invisible Routes

@app.route("/cars/<int:id>/delete")
def delete_car(id):
    # Doing a check to see if someone is not logged in and sending them to the login/reg page if they're not
    if "user_id" not in session:
        return redirect("/")
    data = {
        "id": id
    }
    car.Car.delete_car(data)
    return redirect("/dashboard")