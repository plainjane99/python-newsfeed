# import Base class from app.db
from app.db import Base
# import classes from the sqlalchemy module to define the table columns and their data types
from sqlalchemy import Column, Integer, String
# import sqlalchemy's validation function to validate email address
from sqlalchemy.orm import validates
# import bcrypt to encrypt our user's password information prior to send it to the database
import bcrypt

# create a salt to hash passwords against
# salt is random data that is used as an additional input to a one-way function that hashes passwords/data
salt = bcrypt.gensalt()

# When using SQLAlchemy, we create models as Python classes
# creates a User class that inherits from the Base class
class User(Base):
  __tablename__ = 'users'
  # declare several properties that the parent Base class will use to make the table
  # use classes from the sqlalchemy module to define the table columns and their data types
  # i.e. Column, Integer, String
  # nullable=False will become a SQL 'NOT NULL'
  id = Column(Integer, primary_key=True)
  username = Column(String(50), nullable=False)
  email = Column(String(50), nullable=False, unique=True)
  password = Column(String(100), nullable=False)

  # use validates() function decorator to validate email information
  @validates('email')
  # create a validate_email() method
  def validate_email(self, key, email):
    # make sure email address contains @ character using assert keyword
    # assert keyword automatically throws an error if the condition is false, thus preventing the return statement from happening
    assert '@' in email
    # method returns what the value of the email column should be
    return email

  # use validates() function decorator to validate password information
  @validates('password')
  # create a validate_password() method
  def validate_password(self, key, password):
    # make sure the password is longer than 4 characters
    assert len(password) > 4
    # return the encypted password
    return bcrypt.hashpw(password.encode('utf-8'), salt)