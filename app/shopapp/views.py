from flask import render_template, request, redirect, flash,url_for, jsonify
from . import shopapp
import simplejson as json
import datetime
from forms import ListForm, ItemForm, CategoryForm, ProductForm, ShopForm, units
from .. import db
from ..models import Slist, Category, Product, Item, Shop, ProductSchema, ItemSchema, ListSchema, CategorySchema, ShopSchema
from sqlalchemy import func

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
    prods = db.session.query(Slist.name, func.count(Item.id)).join(Item).group_by(Slist.id)
    prods = dict(prods)

    return render_template('shopapp/shopapp.html',units=units,lists=lists,listForm=listForm,
                           itemForm=itemForm,catForm=catForm, prodForm=prodForm, 
                           shopForm=shopForm, cats=cats,shops=shops,prods=prods)


@shopapp.route('/show_list/<slist>', methods=['GET'])
def show_list(slist):
    prodForm=ProductForm()
    slist=slist = Slist.query.filter_by(name=slist).first()
    items = Item.query.filter_by(slist = slist).all()
    cats = Category.query.all()
    #checked_sum = Item.query().filter_by(chk=True, slist=slist)
    checked_sum=db.session.query(db.func.sum(Item.price)).filter(Item.chk==True,Item.slist==slist).scalar()
    if checked_sum==None:
        checked_sum=0
    return render_template('shopapp/list.html',items=items, cats=cats, itemForm=ItemForm(),prodForm=prodForm,chk=checked_sum)

@shopapp.route('/show_cat/<int:cat_id>', methods=['GET'])
def show_cat(cat_id):
    prodForm=ProductForm()
    prods = Product.query.filter_by(category = Category.query.get(cat_id)).all()
    cat = Category.query.get(cat_id)
    prodForm.category.default=cat.name
    prodForm.process()
    return render_template('shopapp/category.html',prods=prods,prodForm=prodForm,cat=cat)

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

@shopapp.route('/edit-item/<int:item_id>', methods=['POST','GET'])
def editItem(item_id):
    itemForm = ItemForm()
    item = Item.query.get(item_id)
    slist = Slist.query.get(item.slist_id)
    if itemForm.validate_on_submit():
        item.shop = itemForm.shop.data
        item.qnty=itemForm.quantity.data
        item.price=itemForm.price.data
        item.notes=itemForm.notes.data
        db.session.commit()
        return redirect(url_for('shopapp.show_list',slist=slist.name))
    else:
        return redirect(url_for('shopapp.shop_main'))
    
@shopapp.route('/edit-list/<int:list_id>', methods=['POST','GET'])
def editList(list_id):
    listForm = ListForm()
    slist = Slist.query.get(list_id)
    if listForm.validate_on_submit():
        slist.name = listForm.name.data
        slist.note=listForm.note.data
        db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/edit-category/<int:cat_id>', methods=['POST','GET'])
def editCategory(cat_id):
    catForm = CategoryForm()
    cat = Category.query.get(cat_id)
    if catForm.validate_on_submit():
        cat.name = catForm.name.data
        cat.note=catForm.note.data
        db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/edit-shop/<int:shop_id>', methods=['POST','GET'])
def editShop(shop_id):
    shopForm = ShopForm()
    shop = Shop.query.get(shop_id)
    if shopForm.validate_on_submit():
        shop.name = shopForm.name.data
        shop.note=shopForm.note.data
        db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/edit-product/<int:prod_id>', methods=['POST','GET'])
def editProduct(prod_id):
    prodForm = ProductForm()
    prod = Product.query.get(prod_id)
    if prodForm.validate_on_submit():
        prod.name=prodForm.name
        prod.category = prodForm.category.data
        prod.note=prodForm.note.data
        prod.size = prodForm.size.data
        prod.unit=prodForm.unit.data
        db.session.commit()
    return redirect(url_for('shopapp.shop_main'))

@shopapp.route('/check-item/<int:item_id>', methods=['POST'])
def check_item(item_id):
    item=Item.query.get(item_id)
    slist = Slist.query.get(item.slist_id)
    if request.method == 'POST':
        item.chk= not item.chk
        db.session.commit()
    return redirect(url_for('shopapp.show_list',slist=slist.name))

@shopapp.route('/_get_categories',methods=['GET'])
def get_categories():
    products=Category.query.all()
    result=prod_schema.dump(products)
    return jsonify(data=result.data)

@shopapp.route('/_get_category', methods=['GET'])
def get_category():
    cat_id=request.args.get('cat_id')
    cat=Category.query.get(cat_id)
    cat_schema=CategorySchema()
    result=cat_schema.dump(cat)
    return jsonify(data=result.data)

@shopapp.route('/_get_products',methods=['GET'])
def get_products():
    cat=request.args.get('cat')
    prod_schema=ProductSchema(many=True)
    products=Product.query.filter_by(category=Category.query.filter_by(name=cat).first()).all()
    result=prod_schema.dump(products)
    return jsonify(data=result.data)

@shopapp.route('/_get_product', methods=['GET'])
def get_product():
    prod_id=request.args.get('prod_id')
    prod=Product.query.get(prod_id)
    prod_schema=ProductSchema()
    result=prod_schema.dump(prod)
    return jsonify(data=result.data)

@shopapp.route('/_get_item',methods=['GET'])
def get_item():
    item_id=request.args.get('item_id')
    item=Item.query.get(item_id)
    item_schema=ItemSchema()
    result=item_schema.dump(item)
    return jsonify(data=result.data)

@shopapp.route('/_get_list',methods=['GET'])
def get_list():
    list_id=request.args.get('list_id')
    slist=Slist.query.get(list_id)
    list_schema=ListSchema()
    result=list_schema.dump(slist)
    return jsonify(data=result.data)

@shopapp.route('/_get_shop',methods=['GET'])
def get_shop():
    shop_id=request.args.get('shop_id')
    shop=Shop.query.get(shop_id)
    shop_schema=ShopSchema()
    result=shop_schema.dump(shop)
    return jsonify(data=result.data)
