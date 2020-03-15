#!/usr/bin/python3


import modelos
from sqlalchemy import MetaData, Table, Column, String, Integer, Boolean
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as db
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash


Base = declarative_base()

class BaseModel:
    id = Column(String(60), primary_key=True)
    correo = Column(String(60), unique=True)
    telefono = Column(Integer)
    password = Column(String(60))
    nombre = Column(String(60))
    direccion = Column(String(60))
    activo = Column(Boolean, unique=False, default=False)
    
    def __init__(self, *args, **kwargs):
        if kwargs:
             for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
        else:
            pass


    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        modelos.storage.agregar(self)
        modelos.storage.save()
