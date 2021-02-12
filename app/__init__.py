# __init__.py file makes the directory it is in a package
# import the Flask-MySQL connection function we created
from app.db import init_db

from flask import Flask

# import modules directly from routes package
from app.routes import home, dashboard, api

# import filters for use
from app.utils import filters

# this creates a basic flask server
# def = define
def create_app(test_config=None):
  # set up app config
  # declare a new app variable (and it doesn't require var or const) to create the flask instance
  # serve any static resources from the root directory and not from the default /static directory
  app = Flask(__name__, static_url_path='/')
  # Trailing slashes are optional
  # i.e. /dashboard and /dashboard/ load the same route
  app.url_map.strict_slashes = False
  # app uses the key called 'super_secret_key' when creating server-side sessions
  app.config.from_mapping(
    SECRET_KEY='super_secret_key'
  )

  # this turns the function into a route
  @app.route('/hello')
  # this is the function
  def hello():
    return 'hello world'

  # register routes
  app.register_blueprint(home)
  app.register_blueprint(dashboard)

  # create the connection with the database once the flask app is ready
  # pass in app variable we created 
  init_db(app)

  # register the filters we created
  app.jinja_env.filters['format_url'] = filters.format_url
  app.jinja_env.filters['format_date'] = filters.format_date
  app.jinja_env.filters['format_plural'] = filters.format_plural

  # register the api blueprint with the api we created so that any routes we create in api will become part of the Flask app
  # prefix will be /api
  app.register_blueprint(api)

  return app