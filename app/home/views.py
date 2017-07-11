from flask import redirect, render_template, url_for, flash, abort

from . import home

@home.route('/')
def home_main():
    return render_template('home/index.html')
