import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base=declarative_base()


class medicalstore(Base):
    __tablename__='store'

    id =Column(Integer, primary_key=True)
    name =Column(String(250),nullable=False)
    image =Column(String(3050))
    location =Column(String(250),nullable=False)
  

class medicine(Base):
    __tablename__='medicine'
    
    id=Column(Integer, primary_key=True)
    name=Column(String(80), nullable=False)
    expiredate=Column(String(250))
    image =Column(String(3050))
    cost=Column(String(250))


    store_id=Column(Integer, ForeignKey('store.id'))
    store=relationship(medicalstore)


class Signup(Base):
    __tablename__='Signup'

    id =Column(Integer, primary_key=True)
    name =Column(String(250),nullable=False)
    email =Column(String(3050))
    lat =Column(Integer)
    lon =Column(Integer)
    image =Column(String(3050))
    mobile =Column(Integer)
    creatpassword =Column(String(3050))
    conformpassword =Column(String(3050))


engine=create_engine('sqlite:///medi.db')
 

Base.metadata.create_all(engine)
 

