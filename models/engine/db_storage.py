#!/usr/bin/python3
"""the new engine that will be using database instead of filestorage
    module can be imported
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv


class DBStorage:
    """the class that estabishes a connection with the mysql database"""
    __engine = None
    __session = None

    def __init__(self):
        """creates the engine to initiate the connection"""
        from models.base_model import Base
        user = getenv('HBNB_MYSQL_USER')
        paswd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        self.__engine = create_engine(f"mysql+mysqldb://{user}:\
{paswd}@{host}/{database}", pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """querries all the objects that are in the database which are cls
        instances if cls is none is querries all the objects"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        my_dict = {}
        my_list_dict = {'User': User, 'Place': Place,
                        'State': State, 'City': City, 'Amenity': Amenity,
                        'Review': Review}
        if cls is not None:
            query = self.__session.query(cls)
            result = query.all()
            for obj in result:
                key = f"{obj.to_dict()['__class__']}.{obj.id}"
                my_dict[key] = obj
        else:
            for key in my_list_dict.keys():
                query = self.__session.query(my_list_dict[key])
                result = query.all()
                for obj in result:
                    key = f"{obj.to_dict()['__class__']}.{obj.id}"
                    my_dict[key] = obj
        return my_dict

    def new(self, obj):
        """adds the object to the database"""
        self.__session.add(obj)

    def save(self):
        """commits all the changes to the current database"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes an object from the current session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """creates all the tables in the database"""
        from models.base_model import BaseModel, Base
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        #  ScopedSession = scoped_session(Session)
        self.__session = scoped_session(Session)

    def close(self):
        """calls the remove method of the object
        """
        self.__session.remove()
