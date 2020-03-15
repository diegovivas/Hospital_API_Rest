#!/usr/bin/python3
"""
Clase Database encargada de gestionar
todos los elementos en la base de datos.
"""
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
        """
        inicializa la base de datos.
        """
        self.__engine = db.create_engine('postgresql://postgres:passwd@localhost/API_REST_HOSPITAL')
        print("DB instancia creada")
        
    def agregar(self, obj):
        """
        agrega objetos a la base de datos.
        """
        self.__session.add(obj)

    
    def query(self, query):
        """
        trae las tablas en la base de datos y las
        convierte en objetos que son almacenados
        como valores en un diccionario, este es
        el que se retorna al final con las id
        de los objetos como claves.
        """
        objects = {}
        queri = eval(query)
        for row in self.__session.query(queri).all():
            key = str(row.id)
            objects[key] = row
        return objects
    
    def querymail(self, query):
        """
        hace lo mismo que query pero guarda
        las claves con los correos de cada objeto.
        """
        objects = {}
        queri = eval(query)
        for row in self.__session.query(queri).all():
            key = str(row.correo)
            objects[key] = row
        return objects
    
    def query_registros(self):
        """
        retorna todos los registros.
        """
        return self.__session.query(Observacion).all()
        
    def getbyid(self, id):
        """
        retorna u objeto a partir de su id.
        """
        objects = {}
        for element in ["Hospital", "Medico", "Paciente"]:
            objects = self.query(element)
            if id in objects:
                return objects[id]
        return objects


    def getbymail(self,mail):
        """
        retorna un objeto a partir de su mail.
        """
        objects = {}
        for element in ["Hospital", "Medico", "Paciente"]:
            objects = self.querymail(element)
            if id in objects:
                return objects[mail]
        return objects
    
    def es_hospital(self, id):
        """
        verifica si un objeto es de tipo Hospital.
        """
        usuario = self.getbyid(id)
        if "Hospital" in str(usuario.__class__):
            return True
        return False
    
    def es_medico(self, id):
        """
        verifica si un objeto es de tipo Medico.
        """
        usuario = self.getbyid(id)
        if "Medico" in str(usuario.__class__):
            return True
        return False

    def save(self):
        """
        guarda la session pasa la base de datos.
        """
        self.__session.commit()

    def reload(self):
        """
        carda los datos de la base de datos.
        """
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session
        
    def close(self):
        """
            calls remove() on private session attribute (self.session)
        """
        self.__session.remove()

