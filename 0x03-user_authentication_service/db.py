#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine, tuple_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
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
        try:
            user = User(email=email, hashed_password=hashed_password)
            self._session.add(user)
            self._session.commit()
        except Exception:
            # Handle the case when a user with the same email already exists
            self._session.rollback()
            user = None
        return user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by given criteria
        """
        filter_fields, filter_values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                filter_fields.append(getattr(User, key))
                filter_values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*filter_fields).in_([tuple(filter_values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes
        """
        user = self.find_user_by(id=user_id)
        if user is None:
            return
        update_values = {}
        for key, value in kwargs.items():
            if hasattr(User, key):
                update_values[getattr(User, key)] = value
            else:
                raise ValueError()
        self._session.query(User).filter(User.id == user_id).update(
            update_values,
            synchronize_session=False,
        )
        self._session.commit()
