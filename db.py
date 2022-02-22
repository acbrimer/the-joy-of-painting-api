from sqlalchemy import create_engine
from db_schema import Base
import os

print(f'sqlite://{os.getcwd()}/dev.db')

engine = create_engine(f'sqlite:///{os.getcwd()}/dev.db', echo=False)
Base.metadata.create_all(bind=engine, checkfirst=True)
