
from sqlalchemy.sql.schema import MetaData
from sqlalchemy import create_engine
from .db_storage_base import DBStorageBase
from typing import Union


class SQLiteStorage(DBStorageBase):
    """
    Connection instance to Sqlite DB
    """

    SQLITE_DATA_DIR = 'sqlite_data'
    __SQLITE_FILE_NAME: str
    __SQLITE_FILE_PATH: str

    def __init__(self,
                 SQLITE_FILE_NAME: Union[str, None] = None,
                 **kwargs
                 ):
        """Initialize Sqlite connection"""
        print(f"SQLiteStorage.__init__ {SQLITE_FILE_NAME}")
        if SQLITE_FILE_NAME:
            self.__SQLITE_FILE_NAME = SQLITE_FILE_NAME
            self.__SQLITE_FILE_PATH = f"sqlite:///{SQLiteStorage.SQLITE_DATA_DIR}/{self.__SQLITE_FILE_NAME}.db"
        else:
            self.__SQLITE_FILE_NAME = ':memory:'
            self.__SQLITE_FILE_PATH = 'sqlite://'

        self.__engine = create_engine(self.__SQLITE_FILE_PATH)
        self.__metadata = MetaData(bind=self.__engine)

        super().__init__(self.__engine, self.__metadata, **kwargs)
