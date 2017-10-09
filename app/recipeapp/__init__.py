# -*- coding: utf-8 -*-
from flask import Blueprint

recipeapp = Blueprint('recipeapp',__name__,template_folder='templates')

from . import views