from flask import Blueprint

recepieapp = Blueprint('recepieapp',__name__,template_folder='templates')

from . import views