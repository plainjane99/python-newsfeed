# this file is a "module"

# import the Blueprint and render_template functions from flask 
# Blueprint() lets us consolidate routes onto a single bp object
##### This corresponds to using the Router middleware of Express.js
# render_template allows us to return a template (similar to handlebars)
from flask import Blueprint, render_template

# import Post model
from app.models import Post
# import function that returns the session-connection object
from app.db import get_db

# consolidate routes onto a single bp object
bp = Blueprint('home', __name__, url_prefix='/')

# add a @bp.route() decorator before the function to turn it into a route
@bp.route('/')
def index():
  # save returned session connection that's tied to this route's context to db variable
  db = get_db()
  # then we use the query() method on the connection object to query the Post model for all posts
  # in descending order
  # save to posts variable
  # get all posts
  posts = db.query(Post).order_by(Post.created_at.desc()).all()
  # return a template rather than the string homepage.html
  # with posts data
  return render_template(
    'homepage.html',
    posts=posts
)

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
  # save returned session connection that's tied to this route's context to db variable
  db = get_db()
  # get single post by id
  # use the filter() method on the connection object to specify the SQL WHERE clause
  post = db.query(Post).filter(Post.id == id).one()
  # return a template rather than the string single-post.html
  # pass the single post object to the single-post.html template
  # Once the template is rendered and the response sent, 
  # the context for this route terminates, and the teardown function closes the database connection
  # (defined by init_db(app) function in app/db/__init__.py)
  return render_template(
    'single-post.html',
    post=post
  )