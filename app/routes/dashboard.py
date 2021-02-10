# this file is a "module"
# this module is for the dashboard routes

# import the Blueprint and render_template functions from flask 
# Blueprint() lets us consolidate routes onto a single bp object
##### This corresponds to using the Router middleware of Express.js
# render_template allows us to return a template (similar to handlebars)
from flask import Blueprint, render_template

# using the url_prefix argument, we prefix every route in the blueprint with /dashboard
bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

# due to prefix, this route is /dashboard
@bp.route('/')
def dash():
  return render_template('dashboard.html')

# due to prefix, this route is /dashboard/edit/<id>
@bp.route('/edit/<id>')
def edit(id):
  return render_template('edit-post.html')