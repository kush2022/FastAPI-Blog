from sqlalchemy import Column, String, Integer

from blog.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)


class Blog(Base):
    __tablename__ = "blog"
    
    id = Column(Integer, index=True, primary_key=True)
    title = Column(String)
    body = Column(String)
    