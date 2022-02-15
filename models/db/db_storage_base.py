
from sqlalchemy.sql.schema import MetaData
from models.base import Base
from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func, create_mock_engine
from typing import Type


class DBStorageBase:
    """
    Defines a connection to a SQL database using sqlalchemy
    sqlalchemy connection objects
    """
    # initialized for all db classes
    __echo: bool

    # Initialized from child db class
    __engine: Type[Engine]
    __session: Type[scoped_session]
    __metadata: Type[MetaData]

    def __init__(self, engine, metadata, **kwargs):
        self.__engine = engine
        self.__metadata = metadata
        if kwargs:
            for k, v in kwargs.items():
                if k in ['echo']:
                    setattr(self, k, v)
        self.engine.echo = self.echo

    @property
    def metadata(self):
        return self.__metadata

    @property
    def engine(self):
        return self.__engine

    @property
    def session(self):
        return self.__session

    @property
    def echo(self):
        return self.__echo or False

    @echo.setter
    def echo(self, value):
        self.__echo = value

    def get_ddl(self):
        def dump(sql, *multiparams, **params):
            print(sql.compile(dialect=self.__engine.dialect))
        engine = create_mock_engine(f'sqlite://', dump)
        Base.metadata.create_all(engine, checkfirst=False)

    def table_exists(self, table_name):
        """Checks if table exists"""
        return self.__engine.dialect.has_table(self.__engine, table_name)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.engine)
        sess_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get_count(self, cls):
        """Gets rowcount from table"""
        return self.__session.query(func.count(cls.id)).scalar()

    def get_list(self, cls, per_page=10, page=0, sort_field="id", sort_dir="ASC", filter_args={}):
        q = cls.getBaseQuery()
        if len(filter_args.keys()) > 0:
            q = q.filter_by(**filter_args)
        if sort_dir != 'ASC':
            q = q.order_by(cls.__table__.columns[sort_field].desc())
        else:
            q = q.order_by(cls.__table__.columns[sort_field])
        q = q.limit(per_page).offset(page * per_page)
        return {"data": [r.to_dict() for r in q.all()], "total": self.get_count(cls)}

    def get_many(self, cls, ids=[]):
        q = self.__session.query(cls).filter(cls.id.in_(ids))
        return {"data": [r.to_dict() for r in q.all()]}

    def get_many_reference(self, cls, target, id, per_page=10, page=0, sort_field="id", sort_dir="asc", filter_args={},):
        return {"data": [], "total": 0}

    def get_one(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        try:
            res = self.__session.query(cls).filter_by(id=id).one()
            return res
        except NoResultFound as e:
            return None
        except Exception as e:
            return None

    def all(self, cls):
        return self.__session.query(cls).all()
