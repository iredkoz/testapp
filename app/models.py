from app import db,ma
from datetime import datetime
from marshmallow import Schema

# shopping lists table
class Slist(db.Model):
    __tablename__="slist"
    id=db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    note = db.Column('note',db.String(255))
    date = db.Column('date',db.Date,default = datetime.utcnow())
    
#  product categories  
class Category(db.Model):
    __tablename__='category'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    note = db.Column('note',db.String(120))    
    icon = db.Column('icon',db.String(120))# icon name in Font Awesome

# products table    
class Product(db.Model):
    __tablename__='product'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name',db.String(50))
    icon = db.Column('icon',db.String(255)) # icon name or img path?
    note = db.Column('note',db.String(255))
    category_id = db.Column('category_id',db.Integer,db.ForeignKey('category.id'))
    size = db.Column('size',db.Numeric(precision=2, asdecimal=False, decimal_return_scale=None))
    unit = db.Column('unit_id',db.String(50))
    
    category = db.relationship('Category', foreign_keys=category_id, backref='products')

# Shopping list items table
class Item(db.Model):
    __tablename__='item'
    id = db.Column('id',db.Integer,primary_key=True)
    qnty = db.Column('qnty',db.Integer)
    price = db.Column('price',db.Integer)
    chk = db.Column('chk',db.Boolean)
    note = db.Column('note',db.String(255))
    
    slist_id = db.Column('slist_id', db.Integer, db.ForeignKey('slist.id'))
    product_id=db.Column('product_id',db.Integer,db.ForeignKey('product.id'))
    shop_id=db.Column('shop_id',db.Integer,db.ForeignKey('shop.id'))
    
    product = db.relationship('Product',foreign_keys=product_id,backref='items')
    shop = db.relationship('Shop',foreign_keys=shop_id, backref='items')
    slist = db.relationship('Slist', foreign_keys=slist_id, backref='items')
    
class Shop(db.Model):
    __tablename__='shop'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    note = db.Column('note',db.String(255))

class ProductSchema(Schema):
    class Meta:
        fields=('id','name','note','size','unit')

class CategorySchema(Schema):
    class Meta:
        fields=('id','name','note')
