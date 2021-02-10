# this file is a "module"

# import the Blueprint and render_template functions from flask 
# Blueprint() lets us consolidate routes onto a single bp object
##### This corresponds to using the Router middleware of Express.js
# render_template allows us to return a template (similar to handlebars)
from flask import Blueprint, render_template

# consolidate routes onto a single bp object
bp = Blueprint('home', __name__, url_prefix='/')

# add a @bp.route() decorator before the function to turn it into a route
@bp.route('/')
def index():
  # return a template rather than the string homepage.html
  return render_template('homepage.html')

# add a @bp.route() decorator before the function to turn it into a route
@bp.route('/login')
def login():
  # return a template rather than the string login.html
  return render_template('login.html')

# add a @bp.route() decorator before the function to turn it into a route
# use a parameter, represented by <id>
@bp.route('/post/<id>')
# to capture it, we include it as a function parameter
def single(id):
  # return a template rather than the string single-post.html
  return render_template('single-post.html')