#!/usr/bin/env python3
"""
An SQLAlchemy model => User
"""
from sqlalchemy import String, Column, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """
    How the tabke will/shall look like
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
