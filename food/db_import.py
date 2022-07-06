from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData

from django.config.settings import DATABASE_URI

# echo = True --> log all stattements
engine = create_engine('sqlite://' + DATABASE_URI, echo=True)


meta = MetaData()

# define table
students = Table(
	'openfactfood', meta,
	Column("id", Integer, primary_key=True),
	Column("code", String),
	

)

