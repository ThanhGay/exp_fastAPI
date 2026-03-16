from app.models.base import BaseAuth
from sqlalchemy import Column, Integer, String, Float, Text

class User(BaseAuth):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True, index=True)
    username=Column(String(100), nullable=False)
    email=Column(Text)
    password=Column(Text)
    status=Column(Integer)
'''
class Role(BaseAuth):
    __tablename__="Role"

class Permision(BaseAuth):
    __tablename__="Permission"

# User N - N Role
class UserRole(BaseAuth):
    __tablename__="UserRole"

# Role N - N Permission
class RolePermisison(BaseAuth):
    __tablename__="RolePermisison"
'''