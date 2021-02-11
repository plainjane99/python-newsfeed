# __init__.py file makes the directory it is in a package

# import user module in __init__.py file to consolidate modules and make it easier to import them into other modules
from .User import User
from .Post import Post
from .Comment import Comment
from .Vote import Vote