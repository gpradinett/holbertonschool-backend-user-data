#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        method which has two required string arguments:
        email and hashed_password, and returns a User object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        method takes in arbitrary keyword arguments and returns
        the first row found in the users table as filtered by
        the method’s input arguments
        """
        try:
            user_filter = self._session.query(User).filter_by(**kwargs).first()
        except TypeError:
            raise InvalidRequestError

        if user_filter is None:
            raise NoResultFound

        return user_filter

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        method will use find_user_by to locate the user to update,
        then will update the user’s attributes as passed in the method’s
        arguments then commit changes to the database
        """
        user = self.find_user_by(id=user_id)
        names_columns = User.__table__.columns.keys()

        for key in kwargs.keys():
            if key not in names_columns:
                raise ValueError

        for key, value in kwargs.items():
            setattr(user, key, value)
