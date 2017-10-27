from app import db,ma
from datetime import datetime
from marshmallow import Schema, fields, ValidationError, pre_load

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
    note = db.Column('notflase',db.String(120))    
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
    price = db.Column('price',db.Numeric(precision=2))
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
    
class Finances(db.Model):
    __tablename__='finances'
    id = db.Column('id',db.Integer, primary_key=True)
    date = db.Column('date',db.Date,default = datetime.utcnow())
    check_num = db.Column('check_num',db.Integer)
    price = db.Column('price',db.Numeric(precision=2))
    
    shop_id=db.Column('shop_id',db.Integer,db.ForeignKey('shop.id'))

    shop = db.relationship('Shop',foreign_keys=shop_id, backref='finances')
    
class Recipes(db.Model):
    __tablename__='recipes'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    note = db.Column('note',db.String(255))
    category = db.Column('category',db.String(80))
    subcategory = db.Column('subcat',db.String(80))
    food_type = db.Column('food_type',db.String(80))
    prep_time = db.Column('prep_time',db.Time)
    favourite = db.Column('favourite',db.Boolean)

class Photos(db.Model):
    __tablename__='photos'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    filename = db.Column('filename',db.String(255))
    
class Ingridients(db.Model):
    __tablename__='ingridients'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    note = db.Column('note',db.String(255))
    category = db.Column('category',db.String(80))
    
class Steps(db.Model):
    __tablename__='steps'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    name = db.Column('name',db.String(80))
    description = db.Column('description',db.String(2048))
    recipe_id = db.Column('recipe_id',db.Integer,db.ForeignKey('recipes.id'))
    recipe = db.relationship('Recipes',foreign_keys=recipe_id,backref='step_recipes')
    photo_id = db.Column('photo_id', db.Integer, db.ForeignKey('photos.id'))
    photo = db.relationship('Photos', foreign_keys = photo_id, backref='step_photo')
    
class RecipePhotos(db.Model):
    __tablename__='recipe_photos'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    recipe_id = db.Column('recipe_id',db.Integer,db.ForeignKey('recipes.id'))
    recipe = db.relationship('Recipes',foreign_keys=recipe_id,backref='recipe_photo_recipes')
    photo_id = db.Column('photo_id',db.Integer,db.ForeignKey('photos.id'))
    photo = db.relationship('Photos',foreign_keys=photo_id,backref='recipe_photo_photos')

class IngidientList(db.Model):
    __tablename__='ingridient_list'
    __bind_key__='recipe'
    id = db.Column('id',db.Integer,primary_key=True)
    quantity = db.Column('quantity',db.Numeric(precision=2, asdecimal=False, decimal_return_scale=None))
    unit = db.Column('unit',db.String(50))
    
    recipe_id = db.Column('recipe_id',db.Integer,db.ForeignKey('recipes.id'))
    recipe = db.relationship('Recipes',foreign_keys=recipe_id,backref='ingr_list_recipes')
    
    step_id = db.Column('step_id',db.Integer,db.ForeignKey('steps.id'))
    step = db.relationship('Steps',foreign_keys=step_id,backref='ingr_list_steps')
    
    ingridient_id = db.Column('ingridient_id',db.Integer,db.ForeignKey('ingridients.id'))
    ingridient = db.relationship('Ingridients',foreign_keys=ingridient_id,backref='ingr_list_ingridients')
    
    
class CategorySchema(Schema):
    class Meta:
        fields=('id','name','note')

class ProductSchema(Schema):
    id = fields.Int(dump_only=True)
    category = fields.Nested('CategorySchema', only = ('name'))
    name = fields.Str()
    note = fields.Str()
    size = fields.Decimal()
    unit = fields.Str()
#    class Meta:
#        fields=('id','name','note','size','unit','category')

class ShopSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    note = fields.Str()
#    class Meta:
#        fields = ('id','name','note')
        
class ItemSchema(Schema):
    id = fields.Int(dump_only=True)
    product = fields.Nested('ProductSchema', only = ('name'))
    shop = fields.Nested('ShopSchema',only = ('name'))
    qnty = fields.Int()
    price = fields.Decimal()
    note = fields.Str()
        
class ListSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    note = fields.Str()
