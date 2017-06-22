from flask import render_template, request, redirect, flash,url_for, jsonify
from testapp import app
import json
import datetime


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % (error))
            
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/shopapp')
def shopapp():
    return render_template('shopapp.html')

@app.route('/finapp')
def finapp():
    return render_template('financeapp.html')

@app.route('/recepies')
def recepies():
    return render_template('recepieapp.html')