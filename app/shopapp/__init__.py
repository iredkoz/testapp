from flask import Blueprint

shopapp = Blueprint('shopapp',__name__,template_folder='templates')

from . import views