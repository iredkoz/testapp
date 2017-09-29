from flask import redirect, render_template, url_for, flash, abort

from . import recipeapp

@recipeapp.route('/recipes')
def recipes_main():
    return render_template('recipeapp/recipeapp.html')
