# this file is for the api endpoints

# Blueprint is...
# request object is a global contextual object that contains information about the request
# jsonify returns back JSON notation
# session is similar to express-session npm package where we can have the app keep track of user's logged-in status
from flask import Blueprint, request, jsonify, session

from app.models import User, Post, Comment, Vote

# bring in the function for use
from app.db import get_db

# sys module allows us to see error messages
import sys

# import the auth decorator
from app.utils.auth import login_required

# create the api blueprint
bp = Blueprint('api', __name__, url_prefix='/api')

# add routes we need

## use decorator functions
## for function below:
## signup() is 'decorated' by @bp.route function
## the @ character signifies that the function should be treated as a decorator
## signup() function passed into route() function to be called at a later time

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
    # perform the INSERT against the database
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

## this route resolves to /comments and is a POST route
@bp.route('/comments', methods=['POST'])
# add auth decorator
@login_required
def comment():
  # capture the posted data by using the get_json() method
  data = request.get_json()
  db = get_db()

  # use try/except in case creation of comment fails
  try:
    # create a new comment
    newComment = Comment(
      # comment_text and post_id come from user
      # user_id is stored by session
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    # save in database
    ## prep the INSERT statement
    db.add(newComment)
    # perform the INSERT against the database
    db.commit()

  except:
    print(sys.exc_info()[0])

    # discard the pending commit if the INSERT fails
    db.rollback()
    # return a message
    return jsonify(message = 'Comment failed'), 500

  # if the commit is successful, return the the newly created comment ID
  return jsonify(id = newComment.id)

## upvote creates a new record in the votes table but the Post model uses the information
@bp.route('/posts/upvote', methods=['PUT'])
# add auth decorator
@login_required
def upvote():
  # capture the button click by using the get_json() method
  data = request.get_json()
  db = get_db()

  # use try/except in case creation of upvote data fails
  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    # save in database
    ## prep the INSERT statement
    db.add(newVote)
    # perform the INSERT against the database
    db.commit()

  except:
    print(sys.exc_info()[0])

    # discard the pending commit if the INSERT fails
    db.rollback()
    # return a message
    return jsonify(message = 'Upvote failed'), 500

  # if the commit is successful, return 
  return '', 204

# route to create a new post
@bp.route('/posts', methods=['POST'])
# add auth decorator
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

# update the details of a post
# use an <id> route parameter and capture the parameter in the update() function
@bp.route('/posts/<id>', methods=['PUT'])
# add auth decorator
@login_required
# use <id> route parameter in the update() function
def update(id):
  data = request.get_json()
  db = get_db()

  try:
    # SQLAlchemy requires query of the database for the corresponding record
    post = db.query(Post).filter(Post.id == id).one()
    # then update the record like you'd update a normal dictionary
    post.title = data['title']
    # then recommit it
    db.commit()

  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404
  
  return '', 204

# delete a post
# use an <id> route parameter 
@bp.route('/posts/<id>', methods=['DELETE'])
# add auth decorator
@login_required
# pass the <id> parameter into the delete function
def delete(id):
  db = get_db()

  try:
    # SQLAlchemy requires query of the database for the corresponding record
    # then pass the data to db.delete to delete post from db
    db.delete(db.query(Post).filter(Post.id == id).one())
    # commit the change
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204