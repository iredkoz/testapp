from flask import Blueprint

shopapp = Blueprint('shopapp',__name__)

from . import views