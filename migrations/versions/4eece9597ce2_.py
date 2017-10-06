"""empty message

Revision ID: 4eece9597ce2
Revises: 
Create Date: 2017-10-05 11:14:23.244225

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eece9597ce2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()





def upgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade_():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def upgrade_recipe():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ingridients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('note', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=80), nullable=True),
    sa.Column('subcat', sa.String(length=80), nullable=True),
    sa.Column('food_type', sa.String(length=80), nullable=True),
    sa.Column('prep_time', sa.Time(), nullable=True),
    sa.Column('favourite', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recipe_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('steps',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=80), nullable=True),
    sa.Column('description', sa.String(length=2048), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ingridient_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Numeric(precision=2, asdecimal=False), nullable=True),
    sa.Column('unit', sa.String(length=50), nullable=True),
    sa.Column('recipe_id', sa.Integer(), nullable=True),
    sa.Column('step_id', sa.Integer(), nullable=True),
    sa.Column('ingridient_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['ingridient_id'], ['ingridients.id'], ),
    sa.ForeignKeyConstraint(['recipe_id'], ['recipes.id'], ),
    sa.ForeignKeyConstraint(['step_id'], ['steps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('step_photos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('step_id', sa.Integer(), nullable=True),
    sa.Column('photo_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['photo_id'], ['photos.id'], ),
    sa.ForeignKeyConstraint(['step_id'], ['steps.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade_recipe():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('step_photos')
    op.drop_table('ingridient_list')
    op.drop_table('steps')
    op.drop_table('recipe_photos')
    op.drop_table('recipes')
    op.drop_table('photos')
    op.drop_table('ingridients')
    # ### end Alembic commands ###
