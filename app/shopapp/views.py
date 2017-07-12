from flask import render_template, request, redirect, flash,url_for, jsonify
from . import shopapp
import json
import datetime
from forms import ListForm, ItemForm, CategoryForm, ProductForm, ShopForm, units
from .. import db
from ..models import Slist, Category, Product, Item, Shop

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error: %s" % (error))
            

@shopapp.route('/shopmain')
def shop_main():
    listForm = ListForm()
    itemForm = ItemForm()
    catForm = CategoryForm()
    prodForm = ProductForm()
    shopForm = ShopForm()
    
    lists = Slist.query.all()
    cats = Category.query.all()
    shops = Shop.query.all()
    return render_template('shopapp/shopapp.html',units=units,lists=lists,listForm=listForm,
                           itemForm=itemForm,catForm=catForm, prodForm=prodForm, 
                           shopForm=shopForm, cats=cats,shops=shops)

@shopapp.route('/_get_categories',methods=['GET'])
def get_categories():
    products=Category.query.all()
    result=prod_schema.dump(products)
    return jsonify(data=result.data)

@shopapp.route('/show_list/<slist>')
def show_list(slist):
    items = Item.query.filter_by(slist = Slist.query.filter_by(name=slist).first()).all()
    cats = Category.query.all()
    return render_template('shopapp/list.html',items=items, cats=cats)

@shopapp.route('/new-list', methods=['POST'])
def newlist():
    listForm = ListForm()
    name = listForm.name.data
    if listForm.validate_on_submit():
        if Slist.query.filter_by(name=name).first():
            flash('List with this name already exists!','alert-danger')
        else:
            slist = Slist(name=listForm.name.data, date=datetime.datetime.now().date(), note=listForm.note.data)
            db.session.add(slist)
            db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/delete-list/<int:slist_id>', methods=['POST'] )
def delList(slist_id):
    if request.method == 'POST':
        dlist = Slist.query.get(slist_id)
        items = Item.query.filter_by(slist=dlist).all()
        for item in items:
            db.session.delete(item)
        db.session.delete(dlist)
        db.session.commit()
    return ('',204)

@shopapp.route('/new-cat', methods=['POST'])
def newCat():
    catForm = CategoryForm()
    name = catForm.name.data
    if catForm.validate_on_submit():
        if Category.query.filter_by(name=name).first():
            flash('Category already exists!','alert-danger')
        else:
            cat = Category(name=name, note = catForm.note.data)
            db.session.add(cat)
            db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/new-shop', methods=['POST'])
def newShop():
    shopForm = ShopForm()
    name = shopForm.name.data
    if shopForm.validate_on_submit():
        if Shop.query.filter_by(name=name).first():
            flash('Shop already exists!','alert-danger')
        else:
            shop = Shop(name=name, note = shopForm.note.data)
            db.session.add(shop)
            db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

