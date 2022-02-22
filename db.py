from sqlalchemy import create_engine
from db_schema import Base

engine = create_engine('sqlite://', echo=True)
Base.metadata.create_all(engine, checkfirst=True)

