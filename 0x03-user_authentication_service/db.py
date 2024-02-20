#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from user import User, Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
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
        """Add a new user to the database
        """
        user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(user)
            self._session.commit()
            return user
        except IntegrityError:
            # Handle the case when a user with the same email already exists
            self._session.rollback()
            raise ValueError("User with this email already exists")

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given criteria
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound("No user found")
            return user
        except InvalidRequestError:
            # Handle the case of an invalid query
            raise InvalidRequestError("Invalid query arguments")
