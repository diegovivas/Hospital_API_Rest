#!/usr/bin/python3

import sqlalchemy as db
from sqlalchemy.orm import scoped_session, sessionmaker
import modelos
from modelos.base_model import BaseModel, Base
from modelos.hospital import Hospital
from modelos.servicios import Servicio
from modelos.medico import Medico
from modelos.observaciones import Observacion
from modelos.paciente import Paciente

"""
from modelos.medico import Medico, paciente, observaciones
"""
from sqlalchemy import MetaData, Table, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

class Database:
    __engine = None
    __session = None


    def __init__(self):
        self.__engine = db.create_engine('postgresql://postgres:passwd@localhost/API_REST_HOSPITAL')
        print("DB instance created")
        
    def agregar(self, obj):
        self.__session.add(obj)

    
    def query(self, query):
        objects = {}
        queri = eval(query)
        for row in self.__session.query(queri).all():
            key = str(row.id)
            objects[key] = row
        return objects
    
    def querymail(self, query):
        objects = {}
        queri = eval(query)
        for row in self.__session.query(queri).all():
            key = str(row.correo)
            objects[key] = row
        return objects
    
    def query_registros(self):
        return self.__session.query(Observacion).all()
        
    def getbyid(self, id):
        objects = {}
        for element in ["Hospital", "Medico", "Paciente"]:
            objects = self.query(element)
            if id in objects:
                return objects[id]
        return objects


    def getbymail(self, id):
        objects = {}
        for element in ["Hospital", "Medico", "Paciente"]:
            objects = self.querymail(element)
            if id in objects:
                return objects[id]
        return objects
    
    def es_hospital(self, id):
        usuario = self.getbyid(id)
        if "Hospital" in str(usuario.__class__):
            return True
        return False
    
    def es_medico(self, id):
        usuario = self.getbyid(id)
        if "Medico" in str(usuario.__class__):
            return True
        return False

    def save(self):
        self.__session.commit()

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        
    def close(self):
        """
            calls remove() on private session attribute (self.session)
        """
        self.__session.remove()

    def get(self, cls, id):
        """return an object by id and class name from storage"""
        name_of_object = cls + "." + id
        objects = self.all(cls)
        if name_of_object in objects:
            return objects[name_of_object]
        else:
            return None
