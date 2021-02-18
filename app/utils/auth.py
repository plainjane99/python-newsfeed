# create a auth module to protect our routes

from flask import session, redirect
# functools contains helper functions that we can use to change other functions
# wraps() is a decorator itself!
from functools import wraps

# ultimate goal of the Python decorator that we're building is to redirect a user who isn't logged in
# or to run the original route function for a user who is logged in
# define a function called login_required() that expects to receive another function as an argument
# login_required() is the decorator
def login_required(func):
  # @wraps() is the function returned by the login_required() decorator
  # however @wraps() is also a decorator
  @wraps(func)
  # wrapped_function() is the function returned by @wraps decorator
  # *args and **kwargs keywords ensure that no matter how many arguments are given (if any), 
  # the wrapped_function() captures them all
  def wrapped_function(*args, **kwargs):
    # if logged in, call original function with original arguments
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)

    return redirect('/login')
  
  return wrapped_function