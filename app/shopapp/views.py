from flask import render_template, request, redirect, flash,url_for, jsonify
from . import shopapp
import json
import datetime
from forms import ListForm, ItemForm, CategoryForm, ProductForm, units
from .. import db
from ..models import Slist, Category, Product, Item, Shop

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % (error))
            
@shopapp.route('/_get_categories',methods=['GET'])
def get_categories():
    products=Category.query.all()
    result=prod_schema.dump(products)
    return jsonify(data=result.data)
            
@shopapp.route('/')
@shopapp.route('/index')
def index():
    return render_template('shopapp/index.html')

@shopapp.route('/shopmain')
def shopmain():
    listForm=ListForm()
    itemForm = ItemForm()
    catForm = CategoryForm()
    prodForm = ProductForm()
    lists=Slist.query.all()
    return render_template('shopapp/shopapp.html',units=units,lists=lists,listForm=listForm,itemForm=itemForm,
                           catForm=catForm,prodForm=prodForm)

@shopapp.route('/new-list', methods=['POST'])
def newlist():
    form = ListForm()
    name = form.name.data
    if form.validate_on_submit():
        if Slist.query.filter_by(name=name).first():
            flash('List with this name already exists!','alert-danger')
        else:
            slist = Slist(name=form.name.data, date=datetime.datetime.now().date(), note=form.note.data)
            db.session.add(slist)
            db.session.commit()
    return redirect(url_for('shopapp/shopapp'))

