import os
from sqlalchemy import create_engine
from db_schema import Base

engine = create_engine(f'sqlite:///{os.getcwd()}/dev.db',
                       echo=False, connect_args={'check_same_thread': False})
Base.metadata.create_all(bind=engine, checkfirst=True)
