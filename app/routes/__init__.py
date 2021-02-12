# __init__.py file makes the directory it is in a package

# import any variables or functions defined by Python modules into this (or any other) module
# syntax: find the module relatively to the current directory, i.e. "home"
# syntax: import the bp object and rename it home
from .home import bp as home

from .dashboard import bp as dashboard

# import the blueprint we created
from .api import bp as api