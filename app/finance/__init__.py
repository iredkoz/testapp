from flask import Blueprint

finance = Blueprint('finance',__name__,template_folder='templates')

from . import views