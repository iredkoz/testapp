#forms.py
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms.fields import *
from wtforms.validators import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..models import Category,Shop

units = ['lb','oz','gal','qt','pt','fl oz','kg','g','L','ml','box','each','bag','cart',
         'm','cm','mm','inch','ft','yard']

coupons = [u'нет',u'Мп',u'Мк',u'K']

def query_category():
    return Category.query

def query_shop():
    return Shop.query

class ListForm(FlaskForm):
    name = StringField('List Name',render_kw={"placeholder":"ex.List1, List2...","class":"form-control mb-1"},validators=[DataRequired('Please enter list name!')])
    note = TextAreaField('List Note', render_kw={"placeholder":"Notes...", "class":"form-control mb-1"})

class CategoryForm(FlaskForm):
    name = StringField('Category Name',render_kw={"placeholder":"ex.fruits, veggies..","class":"form-control"},validators=[DataRequired('Please enter category name')])
    note = TextAreaField('Category Note',render_kw={"placeholder":"Notes..","class":"form-control"})
    
class ProductForm(FlaskForm):
    name = StringField('Product Name',validators = [DataRequired('Please enter product name')], render_kw={"placeholder":"Gala Apple, Cherry Tomato...","class":"form-control"})
    note = TextAreaField('Product Note', render_kw={"placeholder":"Notes..","class":"form-control"})
    category = QuerySelectField('Category',query_factory=query_category, validators=[DataRequired('Please select product category!')], get_label='name',allow_blank=False, blank_text="All",render_kw={"class":"form-control"})
    size = IntegerField('Product Size', render_kw={"class":"form-control"})
    unit = SelectField('Unit', choices=[(item,item) for item in units],render_kw={"class":"form-control"})
    
class ShopForm(FlaskForm):
    name = StringField('Shop Name',render_kw={"placeholder":"ex.Meijer..","class":"form-control"},validators=[DataRequired('Please enter shop name!')])
    note = TextAreaField('Shop Note', render_kw={"placeholder":"Notes..","class":"form-control"})
    
class ItemForm(FlaskForm):
    product_id = HiddenField('Product',render_kw={"class":"form-control"})
    slist_id = HiddenField('Slist',render_kw={"class":"form-control"})
    shop = QuerySelectField('Shop',query_factory=query_shop, get_label='name',allow_blank=False, blank_text="select Shop",render_kw={"class":"form-control"})
    quantity = IntegerField('Quantity',render_kw={"class":"form-control"})
    price = DecimalField('Price',render_kw={"class":"form-control"})
    notes = TextAreaField('Note',render_kw={"class":"form-control"})
    coupon = SelectField('Coupon', choices=[(item,item) for item in coupons],render_kw={"class":"form-control"})
    