from flask import Flask
# import home module directly from routes package
from app.routes import home, dashboard

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
  
  return app