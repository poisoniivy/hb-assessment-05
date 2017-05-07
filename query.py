"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# A flask SQLAlchemy datatype is returned from the above query.
# In order to retreive the object, can call the mehods .all() for 
# a list of all the items or .one() if there is only one item in the query.


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table is a table in a data model to help build a many-to
# many relationship between two tables. Since many-to-many relationships does
# not technically exist, the association table is the middle table between
# two tables which that creates two one-to-many relationship. The difference
# between a middle table and an association table is middle tables normally
# also have interesting data whereas an association table's sole purpose
# is to just connect two tables in a many-to-many relationship.

# An example being a class that holds Books and another class that is
# Genres. Books may have many genres, and Genres can have many books. An
# association table called "BookGenre" can help with creating the relationship 
# between Books and Genres but technically does not have any other data besides
# the keys to connect to the other two tables.



# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the brand_id of ``ram``.
q1 = Brand.query.filter(Brand.brand_id=='ram').one().name

# Get all models with the name ``Corvette`` and the brand_id ``che``.
q2 = Model.query.filter(Model.name == 'Corvette', Model.brand_id == 'che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year > 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with ``Cor``.
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter(Brand.founded==1903, Brand.discontinued==None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter(db.or_(Brand.founded < 1950, Brand.discontinued != None)).all()

# Get all models whose brand_id is not ``for``.
q8 = Model.query.filter(Model.brand_id!='for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = Model.query.filter(Model.year==year)

    print "Model Name\tBrand Name\tBrand Headquarters"
    for m in models:
        print "%-15s %-15s %s" % (m.name, m.brands.name, m.brands.headquarters)


def get_brands_summary():
    """Prints out each brand name (once) and all of that brand's models,
    including their year, using only ONE database query."""

    brands_and_models = (db.session.query(Brand.name, Model.name, Model.year)
                            .join(Model, Brand.brand_id==Model.brand_id)
                            .order_by(Brand.name))

    brand_name = None
    for b in brands_and_models:
        # Printing brand name just once
        if b[0] != brand_name:
            brand_name = b[0]
            print "************************************"
            print "Brand: ", brand_name
            print "************************************"
        print "%-15s %s" % (b[1], b[2])


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.like('%'+ mystr + '%')).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year, Model.year < end_year).all()
