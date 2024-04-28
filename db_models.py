# cat db_models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .db_sqlalchemy import Base, engine


class Post(Base):
    __tablename__="post_a"
    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    comment=Column(Boolean, server_default='FALSE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("tableusers_a.id",ondelete="CASCADE"),nullable=False)


class User(Base):
    __tablename__="tableusers_a"
    id=Column(Integer, primary_key=True, nullable=False)
    username=Column(String, nullable=False, unique=True)
    #email=Column(str, nullable=False, unique=True)
    passw=Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
