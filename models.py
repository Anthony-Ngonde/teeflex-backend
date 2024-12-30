# Modelling the the database schema
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin


# To ensure consistency in the naming of the constraints, we can define a naming convention that will be used by SQLAlchemy.
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# We then pass the naming convention to the MetaData object
metadata = MetaData(naming_convention=convention)

# We then create an instance of the SQLAlchemy class and pass the metadata object to it
db = SQLAlchemy(metadata=metadata)