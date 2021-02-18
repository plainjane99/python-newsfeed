# this file is a "module"
# this module is for the dashboard routes
from flask import Blueprint, render_template, session
from app.models import Post
from app.db import get_db

# import the auth decorator
from app.utils.auth import login_required

# import the Blueprint and render_template functions from flask 
# Blueprint() lets us consolidate routes onto a single bp object
##### This corresponds to using the Router middleware of Express.js
# render_template allows us to return a template (similar to handlebars)
from flask import Blueprint, render_template

# using the url_prefix argument, we prefix every route in the blueprint with /dashboard
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# due to prefix, this route is /dashboard
@bp.route('/')
# add auth decorator
@login_required
def dash():
  db = get_db()
  # query the database for the corresponding record by user_id
  # order in descending order
  posts = (
    db.query(Post)
    .filter(Post.user_id == session.get('user_id'))
    .order_by(Post.created_at.desc())
    .all()
  )
  return render_template(
    'dashboard.html',
    posts=posts,
    loggedIn=session.get('loggedIn')
  )

# due to prefix, this route is /dashboard/edit/<id>
@bp.route('/edit/<id>')
# add auth decorator
@login_required
def edit(id):
  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()
  return render_template(
    'edit-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  )