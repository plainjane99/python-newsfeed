# This is the Post model which will require some additional functions 
### datetime is a python module to generate timestamps
from datetime import datetime
### need to use ForeignKey and DateTime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, select, func
### relationship allows us to return additional information when other tables are referenced
from sqlalchemy.orm import relationship, column_property
from app.db import Base
from .Vote import Vote

# reminder: SQLAlchemy models written as Python classes
class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True)
  title = Column(String(100), nullable=False)
  post_url = Column(String(100), nullable=False)
  # define as a ForeignKey that references the users table
  user_id = Column(Integer, ForeignKey('users.id'))
  # utilize Python's datetime module
  created_at = Column(DateTime, default=datetime.now)
  updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
  vote_count = column_property(
    #  func.count method counts the number of Vote.id instances from votes model where the post_id is equal to the id of the accessed post
    select([func.count(Vote.id)]).where(Vote.post_id == id)
  )

  # define dynamic properties that won't become part of the MySQL table but that the query will return
  # include a dynamic property for user, 
  # meaning that a query for a post should also return information about its author
  user = relationship('User')
  # query for a post should also return comments
  ### cascade here deletes all associated comments if the post is deleted
  comments = relationship('Comment', cascade='all,delete')