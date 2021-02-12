# this file is for the api endpoints

# Blueprint is...
# request object is a global contextual object that contains information about the request
# jsonify returns back JSON notation
# session is similar to express-session npm package where we can have the app keep track of user's logged-in status
from flask import Blueprint, request, jsonify, session

from app.models import User

# bring in the function for use
from app.db import get_db

# sys module allows us to see error messages
import sys

# create the api blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# add routes we need

## this route resolves to /api/users and is a POST route
@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json()

  # use the function to access the database
  db = get_db()

  # print is similar to console.log
  # using this let's us see the data that was returned in windows powershell
  # in this case, 'data' looks like an object with username, email, and password properties
  # however, it is actually a python 'dictionary' which uses a different notation to access the properties
  #   print(data)

  # add error handling when User model throws an error for bad passwords/email entry by user
  ## attempt to create a user
  try:
    # knowing that the returned data is a dictionary, we pass the properties to a new User model instance
    # note that dictionary properties are accessed with brackets
    newUser = User(
        username = data['username'],
        email = data['email'],
        password = data['password']
    )

    # save in database
    ## prep the INSERT statement
    db.add(newUser)
    ## update the database
    db.commit()

  ## if insertion fails, send an error to the front end 
  ### currently User model has error handling but we need to pass it to the front end as something understandable to the user
  ### send back a message and status code 500 to indicate that a server error occurred
  except:
    # use the sys module to provide developers the error message
    ## AssertionError is thrown when our custom validations fail
    ## IntegrityError is thrown when something specific to MySQL (like a UNIQUE constraint) fails
    print(sys.exc_info()[0])

    # when we 'try' saving data to the database and it fails, the connection remains in a pending state
    # in production, a pending state will crash the app
    # so we need to roll back the commit
    db.rollback()

    # return a message
    return jsonify(message = 'Signup failed'), 500

  # this clears any existing session data then
  # creates two new session properties:
  ## a user_id to add future database queries
  ## and a boolean property that the templates will use to conditionally render statements
  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  # return JSON notation of the new user's id
  return jsonify(id = newUser.id)

## this route resolves to /users/logout and is a POST route
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables and returns 204 status (which indicates that there is no content)
  session.clear()
  return '', 204

## this route resolves to /users/login and is a POST route
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  # step 1 is to check whether the user's email exists
  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    # use the sys module to provide developers the error message
    print(sys.exc_info()[0])
    # tell the user there was a problem and return 400 status code
    return jsonify(message = 'Incorrect credentials'), 400

  # step 2, once email is valid, is to check password
  ## we use the verify_password method we wrote as part of the User model
  ## the incoming data['password'] is actually the second parameter of the verify_password method
  if user.verify_password(data['password']) == False:
    # tell the user there was a problem and return 400 status code
    return jsonify(message = 'Incorrect credentials'), 400

  # this clears any existing session data then
  # creates two new session properties:
  ## a user_id to add future database queries
  ## and a boolean property that the templates will use to conditionally render statements
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True

  # return JSON notation of the user's id
  return jsonify(id = user.id)