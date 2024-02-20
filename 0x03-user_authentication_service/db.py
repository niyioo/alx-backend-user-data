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
        except NoResultFound as e:
            # Handle the case when no user is found
            raise e
        except InvalidRequestError as e:
            # Handle the case of an invalid query
            raise InvalidRequestError("Invalid query arguments") from e

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes
        """
        try:
            user = self.find_user_by(id=user_id)
            for key, value in kwargs.items():
                # Check if the key exists as an attribute in the User model
                if hasattr(User, key):
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")
            self._session.commit()
        except NoResultFound:
            raise ValueError(f"No user found with id: {user_id}")
