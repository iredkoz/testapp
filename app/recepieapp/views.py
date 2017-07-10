from flask import redirect, render_template, url_for, flash, abort

from . import recepieapp

@recepieapp.route('/recepies')
def recepies_main():
    return render_template('recepieapp/recepieapp.html')
