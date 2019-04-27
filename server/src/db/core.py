import datetime

from passlib.hash import bcrypt
from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, Text,
                        text)
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import relationship


"""
General guideline:
ClassName = plural
TableName = singular

server_default specified when possible
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


class UserInviteToken(Base):
    __tablename__ = "user_invite_tokens"

    token_issuer_id = Column(
        Integer, ForeignKey("users.id"), nullable=False, index=True
    )
    token_issuer = relationship("User", foreign_keys="UserInviteToken.token_issuer_id")

    token_user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    token_user = relationship("User", foreign_keys="UserInviteToken.token_user_id")

    token = Column(Text, nullable=False)

    used = Column(Boolean, nullable=False, server_default=text("false"))
    used_datetime = Column(DateTime)

    def set_used(self, token_user):
        self.used = True
        self.used_datetime = datetime.datetime.utcnow()
        self.token_user = token_user
