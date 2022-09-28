from flask_app import app # Import the app
# Add bcrypt for hashing passwords when registering
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

from flask import render_template, request, redirect, session, flash
from flask_app.models import user, car # importing the model files here

# Starting with VISIBLE ROUTES

# creating the root route
@app.route("/")
def index_route():
    return render_template("register_login.html") 


# route to go to the dashboard for new registered users or for users with an existing registration

@app.route("/dashboard")
def go_to_dashboard():
    # need to check if the user is already logged in by checking the session and doing this by creating a data dictionary with the id in session
    if "user_id" in session: # will only show the HTML page if the user is someone logged in
        data = {
            "id": session["user_id"]
        }
        #Getting the user info that's logged in and will show the HTML file
        return render_template("user_dashboard.html", this_user = user.User.get_one_user_by_id(data),\
            all_cars = car.Car.get_all_cars_with_users())
    else: 
        return redirect("/") # if not in session then send user back to the root route



# INVISIBLE ROUTES
    # registering a new user
    # logging in an existing user that's already in the database
    # logging out the user and be sure to clear the session

# Registering a new user route
@app.route("/register_new", methods=["POST"])
def registering_new_user():
    # will need to perform validations on the form first before processing any of the info in the form fields
    # if the validation check fails, will send the user back to the root route
    if not user.User.validating_new_user(request.form): # referencing the method defined in the model file user and class User
        return redirect("/")
    else: # Steps to take when the validation meets requirements and need to hash the password
        # creating a data dictionary to pass the data in from the form
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password']), # hashing the password using bcrypt
        }
        # Then calling on the model to register the new user and placing the user id in a session so we will know this user is logged in when we do a check
        session["user_id"] = user.User.register_new_user(data) # the session variable is created in this line and you can name it what you want
        # redirect the user to the dashboard
        return redirect('/dashboard')



# Logging in an existing user
@app.route("/login_user", methods=["POST"])
def login_existing_user():
    # will need to perform validations on the form first before processing any of the info in the form fields
    # if the validation check fails, will send the user back to the root route
    if not user.User.validate_login_info(request.form):
        return redirect("/")
    else:
        # get the user info from the database
        data = {
            "email": request.form["email"]
        }
        existing_user = user.User.get_one_user_by_email(data)
        # save the user in session
        session["user_id"] = existing_user.id
        return redirect("/dashboard")



# Logs out the user
@app.route("/logout")
def logout_user():
    session.clear() # clears the session
    return redirect("/")    # redirects or sends the user back to the root route with blank fields


