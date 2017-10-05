from flask_wtf import FlaskForm
from flask.ext.uploads import UploadSet, IMAGES
from wtforms.fields import *
from wtforms.validators import *
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from ..models import Recipes, Ingridients, Steps, StepPhotos, RecipePhotos,IngidientList
import constants

images = UploadSet('images',IMAGES)

class IngridientForm(FlaskForm):
    name = StringField('Ingridient Name',validators = [DataRequired('Please enter ingridient name')], render_kw={"placeholder":"Flour, oil, salt..","class":"form-control"})
    note = TextAreaField('Product Note', render_kw={"placeholder":"Notes..","class":"form-control"})
    cat = SelectField('Category', choices=[(item,item) for item in constants.categories],render_kw={"class":"form-control"})

class StepForm(FlaskForm):
    description = TextAreaField('Description',render_kw={"placeholder":"What to do..","class":"form-control"})    
    photo = FileField('Picture',validators = [FileRequired(),FileAllowed(images,'Images only!')])

