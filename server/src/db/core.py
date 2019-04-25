from passlib.hash import bcrypt
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text, text
from sqlalchemy.ext.declarative import as_declarative


"""
General guideline:
ClassName = plural
TableName = singular
"""


@as_declarative()
class Base(object):

    id = Column(Integer, primary_key=True)

    created_datetime = Column(
        DateTime, server_default=text("(now() at time zone 'utc')"), nullable=False
    )


class User(Base):
    __tablename__ = "users"

    username = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = bcrypt.encrypt(password)

    def validate_password(self, password):
        return bcrypt.verify(password, self.password)


class Message(Base):
    __tablename__ = "messages"

    user_id = Column(Integer, ForeignKey("users.id"))

    message = Column(Text, nullable=False)

    sent_datetime = Column(DateTime, nullable=False)
