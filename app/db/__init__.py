# __init__.py file makes the directory it is in a package

# Flask creates a new context every time a server request is made. 
# When the request ends, the context is removed from the app. 
# These temporary contexts provide global variables, like the g object, 
# that can be shared across modules as long as the context is still active
from flask import g

# getenv() function is part of Python's built-in os module
from os import getenv

# import class functions from sqlalchemy
### map the models to MySQL tables
from sqlalchemy.ext.declarative import declarative_base
### to manage overall connection to database
from sqlalchemy import create_engine
### generate temporary connections for CRUD operations
from sqlalchemy.orm import sessionmaker

# call load_dotenv() from the python-dotenv module
# since in development, we use a .env file to fake the environment variable
# in production, DB_URL will be a proper environment variable
from dotenv import load_dotenv

load_dotenv()

# connect to database using env variable
### create the connection to the database
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
# create Session class for connection for CRUD operations
Session = sessionmaker(bind=engine)
# create a Base class variable to map the models to MySQL tables
Base = declarative_base()

# this connects the flask app to the MySQL database
# define the init_db function with app parameter passed in
# call the base.metadata.create_all() method
# which uses the Base class with the engine connection variable we created to build tables that Base has mapped
# then have flask run close_db() together with its built-in teardown_appcontext() method
def init_db(app):
  Base.metadata.create_all(engine)
  app.teardown_appcontext(close_db)

# define a function to return a new session-connection object
# save the current connection on the 'g' object if it's not already there
# return the connection from the 'g' object instead of create a new session instance every time
def get_db():
  if 'db' not in g:
    # store db connection in app context
    g.db = Session()
  return g.db

# we need to remember to close the connection to the database so that the app doesn't crash in production
# creating a function allows us to avoid adding db.close to every route we create
def close_db(e=None):
  # pop() method attempts to find and remove db from the g object
  db = g.pop('db', None)
  # If db exists (that is, db doesn't equal None), then db.close() will end the connection
  if db is not None:
    db.close()