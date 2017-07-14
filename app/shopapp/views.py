from flask import render_template, request, redirect, flash,url_for, jsonify
from . import shopapp
import json
import datetime
from forms import ListForm, ItemForm, CategoryForm, ProductForm, ShopForm, units
from .. import db
from ..models import Slist, Category, Product, Item, Shop, ProductSchema

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

@shopapp.route('/show_list/<slist>', methods=['GET'])
def show_list(slist):
    prodForm=ProductForm()
    items = Item.query.filter_by(slist = Slist.query.filter_by(name=slist).first()).all()
    cats = Category.query.all()
    return render_template('shopapp/list.html',items=items, cats=cats, itemForm=ItemForm(),prodForm=prodForm)

@shopapp.route('/show_cat/<int:cat_id>', methods=['GET'])
def show_cat(cat_id):
    prodForm=ProductForm()
    prods = Product.query.filter_by(category = Category.query.get(cat_id)).all()
    return render_template('shopapp/category.html',prods=prods,prodForm=prodForm)

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

@shopapp.route('/delete-product/<int:prod_id>', methods=['POST'] )
def delProduct(prod_id):
    if request.method == 'POST':
        prod = Product.query.get(prod_id)
        db.session.delete(prod)
        db.session.commit()
    return ('',204)

@shopapp.route('/delete-item/<int:item_id>', methods=['POST'] )
def delItem(item_id):
    if request.method == 'POST':
        item = Item.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
    return ('',204)

@shopapp.route('/delete-cat/<int:cat_id>', methods=['POST'] )
def delCat(cat_id):
    if request.method == 'POST':
        cat = Category.query.get(cat_id)
        db.session.delete(cat)
        db.session.commit()
    return ('',204)

@shopapp.route('/delete-shop/<int:shop_id>', methods=['POST'] )
def delShop(shop_id):
    if request.method == 'POST':
        shop = Shop.query.get(shop_id)
        db.session.delete(shop)
        db.session.commit()
    return ('',204)

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

@shopapp.route('/new-product', methods=['POST'])
def newProduct():
    prodForm = ProductForm()
    name = prodForm.name.data
    if prodForm.validate_on_submit():
        if Product.query.filter_by(name=name).first():
            flash('Product with this name already exists!', 'alert-danger')
        else:
            prod = Product(name=name, category = prodForm.category.data, note=prodForm.note.data, size = prodForm.size.data, unit=prodForm.unit.data)
            db.session.add(prod)
            db.session.commit()
    return redirect(url_for('shopapp.shop_main')) 

@shopapp.route('/new-item', methods=['POST'])
def newItem():
    itemForm = ItemForm()
    if itemForm.validate_on_submit():
        product=Product.query.filter_by(name=itemForm.product_id.data).first()
        slist = Slist.query.filter_by(name=itemForm.slist_id.data).first()
        shop=itemForm.shop.data
        qnty=itemForm.quantity.data
        price=itemForm.price.data
        notes=itemForm.notes.data
        item = Item(product=product, shop = shop, qnty=qnty, price = price, chk = False, note=notes, slist=slist)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('shopapp.show_list',slist=slist.name))
    else:
        return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/check-item/<int:item_id>', methods=['POST'])
def check_item(item_id):
    item=Item.query.get(item_id)
    slist = Slist.query.get(item.slist_id)
    if request.method == 'POST':
        item.chk= not item.chk
        db.session.commit()
    return redirect(url_for('shopapp.show_list',slist=slist.name))

@shopapp.route('/_get_products',methods=['GET'])
def parse_data():
    cat=request.args.get('cat')
    prod_schema=ProductSchema(many=True)
    products=Product.query.filter_by(category=Category.query.filter_by(name=cat).first()).all()
        
    result=prod_schema.dump(products)
    return jsonify(data=result.data)