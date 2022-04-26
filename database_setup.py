import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin

Base=declarative_base()

class Disease(Base):
    __tablename__='disease'

    id =Column(Integer, primary_key=True)
    name =Column(String(250),nullable=False)
    image =Column(String(3050))
    symptmos =Column(String(250))

    # @property
    # def serialize(self):
    #     return 


class Contact(Base,UserMixin):
    __tablename__='Contact'

    id =Column(Integer, primary_key=True)
    name =Column(String(250),nullable=False)
    email =Column(String(3050))
    comments =Column(String(250))



class Sub_disease(Base):
    __tablename__='Sub_disease'
    
    id=Column(Integer, primary_key=True)
    name=Column(String(80), nullable=False)
    description=Column(String(250))
    medicine=Column(String(250))
    treatment=Column(String(250))

    disease_id=Column(Integer, ForeignKey('disease.id'))
    disease=relationship(Disease)



class MedicinesInventoryList(Base):
    __tablename__='MedicinesInventoryList'

    drugid =Column(Integer, primary_key=True)
    drugname =Column(String(250),nullable=False)
    dosage =Column(String(250))
    form =Column(Integer)
    lat =Column(Integer)
    lon =Column(Integer)
    signup_id =Column(Integer)
  
    

# class Medicine(Base):
#     __tablename__='medicine'
    
#     id=Column(Integer, primary_key=True)
#     name=Column(String(80), nullable=False)
#     expiredate=Column(String(250))
#     image =Column(String(3050))
#     cost=Column(String(250))



#     store_id=Column(Integer, ForeignKey('store.id'))
#     store=relationship(MedicalStore)


class Signup(Base,UserMixin):
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



class Ayurvedic(Base):
    __tablename__='ayurvedic'

    id =Column(Integer, primary_key=True)
    name =Column(String(250),nullable=False)
    image =Column(String(3050))
    symptmos =Column(String(250))


class Sub_ayurvedic(Base):
    __tablename__='Sub_ayurvedic'
    
    id=Column(Integer, primary_key=True)
    name=Column(String(80), nullable=False)
    description=Column(String(250))
    medicine=Column(String(250))
    treatment=Column(String(250))

    ayurvedic_id=Column(Integer, ForeignKey('ayurvedic.id'))
    ayurvedic_details=relationship(Ayurvedic)

    

# class medicalstore(Base):
#     __tablename__='store'

#     id =Column(Integer, primary_key=True)
#     name =Column(String(250),nullable=False)
#     image =Column(String(3050))
#     location =Column(String(250),nullable=False)


engine=create_engine('sqlite:///doc.db')
 

Base.metadata.create_all(engine)
