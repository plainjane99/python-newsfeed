# __init__.py file makes the directory it is in a package

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